from etl.SpatialEtl import SpatialEtl


class GSheetsEtl(SpatialEtl):
    def __int__(self, remote, local_dir, data_format, destination):
        super().__int__(remote, local_dir, data_format, destination)

    def process(self):
        super().extract()
        super().transform()
        super().load()
