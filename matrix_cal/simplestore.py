import os
import applogger

logger = applogger.getLogger("SimpleStorage")

paths = os.path

class SimpleStorage(object):

    supported_persisters = ["yaml", "json"]
    _yaml_methods = ["safe_dump", "safe_load"]
    _json_methods = ["dumps", "loads"]

    def __init__(self, path='./.simplestore', persister="json", **elements):

        self._path = path
        self._ensure_pathvalid()
        self._dicts = dict(**elements)
        self._persister = persister
        self._ensure_persistervalid()
        self._import_supported_persisters()

    def _ensure_pathvalid(self):
        if not paths.exists(self._path):
            self.create_new_storefile()

    def _ensure_persistervalid(self):
        if not self._persister in self.supported_persisters:
            raise AttributeError("Non-Supported Persisters Name")
    
    def _import_supported_persisters(self):
        self._persist_map = { k: __import__(k, globals(), locals()) for k in self.supported_persisters }

    def _get_dumps(self, persister):
        p = self._persist_map[persister]
        methods_name = getattr(self, "_%s_methods" % persister)[0]
        return getattr(p, methods_name)

    def _get_loads(self, persister):
        p = self._persist_map[persister]
        methods_name = getattr(self, "_%s_methods" % persister)[1]
        return getattr(p, methods_name)

    def create_new_storefile(self):
        with open(self._path, "w") as f:
            f.write("")
    
    def clear_storagefile(self):
        os.remove(self._path)
        self.create_new_storefile()

    def load_from_disk(self):
        with open(self._path, 'r') as f:
            oristr = f.read()
            if not oristr:
                return
            ori_persiter, ori_data = oristr.split("|||")
            amap = self._get_loads(ori_persiter)(ori_data)
            amap.update(self._dicts)
            self._dicts.update(amap)

    def __getattr__(self, name):
        return self._dicts[name]

    def save_to_disk(self):
        with open(self._path, 'w') as f:
            serializestr = self._get_dumps(self._persister)(self._dicts)
            f.write(self._persister)
            f.write("|||")
            f.write(serializestr)
            f.write("\n")

if __name__ == "__main__":
    """simple file base configuration store"""
    #storage = SimpleStorage(name="qiuli", age=29, profession="coder", matrix=[[0, 0, 0, 1], [1, 0, 0, 0]])
    #storage.clear_storagefile()
    #storage.save_to_disk()
    st = SimpleStorage(persister="yaml")
    st.load_from_disk()

    print st._dicts
