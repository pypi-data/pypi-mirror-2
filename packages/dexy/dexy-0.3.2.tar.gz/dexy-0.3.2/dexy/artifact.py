from dexy.version import VERSION
from ordereddict import OrderedDict
import hashlib
import inspect
import os
import shutil
import time

class Artifact(object):
    META_ATTRS = [
        'binary',
        'key',
        'ext',
        'stdout'
    ]

    HASH_WHITELIST = [
        'args',
        'article_class_source',
        'dexy_version',
        'dirty',
        'dirty_string',
        'ext',
        'handler_source',
        'handler_version',
        'inputs',
        'input_data_dict',
        'input_ext',
        'key'
    ]

    BINARY_EXTENSIONS = [
        '.gif',
        '.jpg',
        '.png',
        '.pdf',
        '.zip',
        '.tgz',
        '.gz',
        '.eot',
        '.ttf',
        '.woff'
    ]

    def __init__(self, key):
        self.key = key
        self.dirty = False
        self.final = None
        self.additional = None
        self.binary = None
        self.args = {}
        self._inputs = {}
        self.data_dict = OrderedDict()
        self.dexy_version = VERSION
        self.article_class_source = inspect.getsource(self.__class__)

    @classmethod
    def setup(klass, doc, key, previous_artifact = None):
        art = klass(key)
        art.setup_from_doc(doc)
        if previous_artifact:
            art.setup_from_previous_artifact(previous_artifact)
        return art

    def add_input(self, key, artifact):
        print "adding input", key
        print "canonical filename", artifact.canonical_filename()
        self._inputs[key] = artifact

    def inputs(self):
        return self._inputs

    def set_binary_from_ext(self):
        # TODO list more binary extensions or find better way to do this
        if self.ext in self.BINARY_EXTENSIONS:
            self.binary = True
        else:
            self.binary = False

    def setup_from_doc(self, doc):
        self.doc = doc
        self.controller = doc.controller
        self.artifacts_dir = doc.controller.artifacts_dir
        self.args = self.doc.args
        if self.args.has_key('final'):
            self.final = self.args['final']
        self.ext = os.path.splitext(doc.name)[1]
        self.set_binary_from_ext()
        self._inputs = doc.input_artifacts()

    def setup_from_previous_artifact(self, previous_artifact):
        if self.final is None:
            self.final = previous_artifact.final
        self.input_ext = previous_artifact.ext
        self.input_data_dict = previous_artifact.data_dict
        self.previous_artifact_filename = previous_artifact.filename()

        self._inputs.update(previous_artifact.inputs())
        # Need to loop over each artifact's inputs in case extra ones have been
        # added anywhere.
        for k, a in previous_artifact.inputs().items():
            self._inputs.update(a.inputs())

    def set_data(self, data):
        self.data_dict['1'] = data

    def set_data_from_artifact(self):
        f = open(self.filepath())
        self.data_dict['1'] = f.read()

    def is_loaded(self):
        return hasattr(self, 'data_dict') and len(self.data_dict) > 0

    def hash_dict(self):
        """Return the elements for calculating the hashstring."""
        if self.dirty:
            self.dirty_string = time.gmtime()

        hash_dict = self.__dict__.copy()

        hash_dict['inputs'] = {}
        for k, a in hash_dict.pop('_inputs').items():
            hash_dict['inputs'][k] = a.hashstring

        # Remove any items which should not be included in hash calculations.
        for k in hash_dict.keys():
            if not k in self.HASH_WHITELIST:
                del hash_dict[k]

        return hash_dict

    def set_hashstring(self):
        hash_data = str(self.hash_dict())
        self.hashstring = hashlib.md5(hash_data).hexdigest()

    def command_line_args(self):
        """
        Allow specifying command line arguments which are passed to the filter
        with the given key. Note that this does not currently allow
        differentiating between 2 calls to the same filter in a single document.
        """
        if self.doc.args.has_key('args'):
            args = self.doc.args['args']
            last_key = self.key.rpartition("|")[-1]
            if args.has_key(last_key):
                return args[last_key]

    def input_text(self):
        text = ""
        for k, v in self.input_data_dict.items():
            text += v
        return text

    def output_text(self):
        text = ""
        for k, v in self.data_dict.items():
            text += v
        return text

    def write_to_file(self, filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        shutil.copyfile(self.filepath(), filename)

    def work_filename(self):
        return "%s.work%s" % (self.hashstring, self.input_ext)

    def generate_workfile(self, work_filename = None):
        if not work_filename:
            work_filename = self.work_filename()
        work_path = os.path.join(self.artifacts_dir, work_filename)
        work_file = open(work_path, "w")
        work_file.write(self.input_text())
        work_file.close()

    def temp_filename(self, ext):
        return "%s.work%s" % (self.hashstring, ext)

    def open_tempfile(self, ext):
        tempfile_path = os.path.join(self.artifacts_dir, self.temp_filename(ext))
        open(tempfile_path, "w")

    def temp_dir(self):
        return os.path.join(self.artifacts_dir, self.hashstring)

    def create_temp_dir(self):
        shutil.rmtree(self.temp_dir(), ignore_errors=True)
        os.mkdir(self.temp_dir())

    def canonical_basename(self):
        return os.path.basename(self.canonical_filename())

    def canonical_filename(self):
        fn = os.path.splitext(self.key.split("|")[0])[0]
        return "%s%s" % (fn, self.ext)

    def long_canonical_filename(self):
        return "%s%s" % (self.key.replace("|", "-"), self.ext)

    def filename(self):
        if not hasattr(self, 'ext'):
            raise Exception("artifact %s has no ext" % self.key)
        return "%s%s" % (self.hashstring, self.ext)

    def filepath(self):
        return os.path.join(self.artifacts_dir, self.filename())

