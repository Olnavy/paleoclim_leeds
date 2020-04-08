import processing as proc
import zones
import numpy as np
import xarray as xr
import util_hadcm3 as util
import abc
import cftime


class HadCM3DS(proc.ModelDS):
    MONTHS = ['ja', 'fb', 'mr', 'ar', 'my', 'jn', 'jl', 'ag', 'sp', 'ot', 'nv', 'dc']
    
    def __init__(self, experiment, start_year, end_year, month_list, verbose, logger):
        super(HadCM3DS, self).__init__(verbose, logger)
        self.lon = None
        self.lat = None
        self.z = None
        self.lon_b = None
        self.lat_b = None
        self.z_b = None
        self.t = None
        self.lsm = None
        self.start_year = start_year
        self.end_year = end_year
        if month_list is None:
            self.months = None
        elif month_list == "full":
            self.months = self.MONTHS
        else:
            self.months = month_list
        
        self.import_data(experiment)
    
    @abc.abstractmethod
    def import_data(self, experiment):
        pass
    
    @abc.abstractmethod
    def import_coordinates(self):
        pass
    
    def get(self, data, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None,
            mode_z=None, value_z=None, mode_t=None, value_t=None, new_start_year=None, new_end_year=None,
            new_month_list=None):
        
        # if type(data_array) is not proc.GeoDataArray:
        #   convert_to_GeoDataArray(data_array)
        
        geo_da = proc.GeoDataArray(data, ds=self)  # add the GeoDataArray wrapper
        try:
            if new_start_year is not None and new_start_year <= self.start_year:
                raise ValueError("The new start year is smaller than the imported one.")
            elif new_end_year is not None and new_end_year >= self.end_year:
                raise ValueError("The new end year is larger than the imported one.")
            elif new_start_year is None and new_end_year is not None:
                geo_da.truncate_years(self.start_year, new_end_year)
            elif new_start_year is not None and new_end_year is None:
                geo_da.truncate_years(new_start_year, self.end_year)
            elif new_start_year is not None and new_end_year is not None:
                geo_da.truncate_years(new_start_year, new_end_year)
            else:
                pass
            
            if new_month_list is not None and self.months is None:
                raise ValueError(f"The month truncation is not available with {type(self)}.")
            elif new_month_list is not None and \
                not all(month in util.months_to_number(self.months) for month in util.months_to_number(new_month_list)):
                raise ValueError("The new month list include months not yet imported.")
            elif new_month_list is not None:
                geo_da.truncate_months(new_month_list)
            else:
                pass
        
        except ValueError as error:
            print(error)
            print("The truncation was aborted.")
        
        geo_da.get_lon(mode_lon, value_lon)
        geo_da.get_lat(mode_lat, value_lat)
        geo_da.get_z(mode_z, value_z)
        geo_da.get_t(mode_t, value_t)
        
        geo_da.fit_coordinates_to_data()
        
        return zone.import_coordinates_from_data_array(geo_da.data).compact(geo_da)
    
    def extend(self,geo_data_array):
        pass
    
    
# **************
# MONTH DATASETS
# **************

class HadCM3RDS(HadCM3DS):
    
    def __init__(self, experiment, start_year, end_year, file_name, month_list, verbose, logger):
        self.buffer_name = "None"
        self.buffer_array = None
        self.file_name = file_name
        self.paths = []
        super(HadCM3RDS, self).__init__(experiment, start_year, end_year, month_list, verbose, logger)
        
        try:
            self.sample_data = xr.open_dataset(self.paths[0])
        except IndexError as error:
            print("No dataset to import. Please check again the import options.")
            raise error
        except FileNotFoundError as error:
            print("The file was not found. Data importation aborted.")
            raise error
        
        self.import_coordinates()
    
    def import_data(self, experiment):
        try:
            path = util.path2expds[experiment]
            self.paths = [f"{path}{self.file_name}{year:09d}{month}+.nc"
                          for year in np.arange(int(self.start_year), int(self.end_year) + 1)
                          for month in self.months]
        except KeyError as error:
            print("This experiment was not found in \"Experiment_to_filename\". Data importation aborted.")
            print(error)
    
    def import_coordinates(self):
        super(HadCM3RDS, self).import_coordinates()
        self.t = None


class OCNMDS(HadCM3RDS):
    """
    PF
    """
    
    def __init__(self, experiment, start_year, end_year, month_list="full", verbose=False, logger="print"):
        file_name = f"pf/{experiment}o#pf"
        super(OCNMDS, self).__init__(experiment, start_year, end_year, file_name=file_name, month_list=month_list,
                                     verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(OCNMDS, self).import_coordinates()
        
        self.lon = self.sample_data.longitude.values
        lon_1 = self.sample_data.longitude_1.values
        self.lon_b = np.append(lon_1, 2 * lon_1[-1] - lon_1[-2])
        
        self.lat = self.sample_data.latitude.values
        lat_1 = self.sample_data.latitude_1.values
        self.lat_b = np.append(lat_1, 2 * lat_1[-1] - lat_1[-2])
        
        self.z = self.sample_data.depth.values
        depth_1 = self.sample_data.depth_1.values
        self.z_b = np.append(depth_1, 2 * depth_1[-1] - depth_1[-2])
    
    def sst(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None, mode_t=None,
            value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = xr.open_mfdataset(self.paths).temp_mm_uo.isel(unspecified=0).drop("unspecified")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)
    
    def temperature(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None,
                    mode_z=None, value_z=None, mode_t=None, value_t=None, new_start_year=None, new_end_year=None,
                    new_month_list=None):
        data_array = xr.open_mfdataset(self.paths).temp_mm_dpth.rename({'depth_1': 'z'})
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, mode_z, value_z, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class OCNYDS(HadCM3RDS):
    """
    PG
    """
    
    def import_coordinates(self):
        super(OCNYDS, self).import_coordinates()
        
        self.lon = self.sample_data.longitude.values
        lon_1 = self.sample_data.longitude_1.values
        self.lon_b = np.append(lon_1, 2 * lon_1[-1] - lon_1[-2])
        
        self.lat = self.sample_data.latitude.values
        lat_1 = self.sample_data.latitude_1.values
        self.lat_b = np.append(lat_1, 2 * lat_1[-1] - lat_1[-2])
        
        self.z = self.sample_data.depth.values
        depth_1 = self.sample_data.depth_1.values
        self.z_b = np.append(depth_1, 2 * depth_1[-1] - depth_1[-2])


class ATMUPMDS(HadCM3RDS):
    """
    PC
    """
    
    def import_coordinates(self):
        super(ATMUPMDS, self).import_coordinates()
        
        self.lon = self.sample_data.longitude.values
        lon_1 = self.sample_data.longitude_1.values
        self.lon_b = np.append(lon_1, 2 * lon_1[-1] - lon_1[-2])
        
        self.lat = self.sample_data.latitude.values
        self.lat_b = self.sample_data.latitude_1.values
        
        self.z = self.sample_data.depth.values
        self.z_b = util.guess_bounds(self.z)


class ATMSURFMDS(HadCM3RDS):
    """
    PD
    """
    
    def import_coordinates(self):
        super(ATMSURFMDS, self).import_coordinates()
        
        self.lon = self.sample_data.longitude.values
        lon_1 = self.sample_data.longitude_1.values
        self.lon_b = np.append(lon_1, 2 * lon_1[-1] - lon_1[-2])
        
        self.lat = self.sample_data.latitude.values
        lat_1 = self.sample_data.latitude_1.values
        self.lat_b = np.append(lat_1, 2 * lat_1[-1] - lat_1[-2])
        
        self.z = self.sample_data.level6.values
        self.z_b = util.guess_bounds(self.z)


class LNDMDS(HadCM3RDS):
    """
    PT
    """
    
    def import_coordinates(self):
        super(LNDMDS, self).import_coordinates()
        
        self.lon = self.sample_data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.sample_data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
        
        self.z = self.sample_data.pseudo.values
        self.z_b = util.guess_bounds(self.z)
        
        # What to do of pseudo pseudo_2 and pseudo_3?


# ***********
# TIME SERIES
# ***********


class HadCM3TS(HadCM3DS):
    
    def __init__(self, experiment, start_year, end_year, file_name, month_list, verbose, logger):
        
        self.data = None
        self.buffer_name = "None"
        self.buffer_array = None
        self.file_name = file_name
        super(HadCM3TS, self).__init__(experiment, start_year, end_year, month_list, verbose, logger)
        
        self.import_coordinates()
    
    def import_data(self, experiment):
        
        try:
            
            path = util.path2expts[experiment]
            self.data = xr.open_dataset(f"{path}{experiment}.{self.file_name}.nc")
            
            if min(self.data.t.values).year >= self.start_year or max(self.data.t.values).year <= self.end_year:
                raise ValueError(f"Inavlid start_year or end_year. Please check that they fit the valid range\n"
                                 f"Valid range : start_year = {min(self.data.t.values).year}, "
                                 f"end_year = {max(self.data.t.values).year}")
            
            # The where+lamda structure is not working (GitHub?) so each steps are done individually
            # .where(lambda x: x.t >= cftime.Datetime360Day(self.start_year, 1, 1), drop=True) \
            # .where(lambda x: x.t >= cftime.Datetime360Day(self.end_year, 12, 30), drop=True)
            # .where(lambda x: x.t.month in util.months_to_number(self.months), drop=True)
            self.data = self.data.where(self.data.t >= cftime.Datetime360Day(self.start_year, 1, 1), drop=True)
            self.data = self.data.where(self.data.t <= cftime.Datetime360Day(self.end_year, 12, 30), drop=True)
            self.data = proc.filter_months(self.data, self.months)
            # data is a xarray.Dataset -> not possible to use xarray.GeoDataArray methods. How to change that?
        
        except FileNotFoundError as error:
            print("The file was not found. Data importation aborted.")
            print(error)
        except KeyError as error:
            print("This experiment was not found in \"Experiment_to_filename\". Data importation aborted.")
            print(error)
    
    def import_coordinates(self):
        super(HadCM3TS, self).import_coordinates()
        self.t = self.data.t.values


class SATMTS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list="full", verbose=False, logger="print"):
        self.data = None
        super(SATMTS, self).__init__(experiment, start_year, end_year, file_name="tempsurf.monthly",
                                     month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(SATMTS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def sat(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None, mode_t=None,
            value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.temp_mm_srf.isel(surface=0).drop("surface")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class SSTATS(HadCM3TS):
    
    def __init__(self, experiment, start_year=None, end_year=None, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(SSTATS, self).__init__(experiment, start_year, end_year, file_name="oceantemppg01.annual",
                                     month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(SSTATS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def sst(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None,
            mode_z=None, value_z=None, mode_t=None, value_t=None, new_start_year=None, new_end_year=None,
            new_month_list=None):
        data_array = self.data.temp_ym_dpth.isel(depth_1=0).drop("depth_1")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, mode_z, value_z, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class SOLTOAMTS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(SOLTOAMTS, self).__init__(experiment, start_year, end_year, file_name="downsolar_toa.monthly",
                                        month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(SOLTOAMTS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def downsol_toa(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None,
                    mode_t=None,
                    value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.downSol_mm_TOA.isel(toa=0).drop("toa")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class EVAPMTS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(EVAPMTS, self).__init__(experiment, start_year, end_year, file_name="evap2.monthly",
                                      month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(EVAPMTS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        lon_1 = self.data.longitude_1.values
        self.lon_b = np.append(lon_1, 2 * lon_1[-1] - lon_1[-2])
        
        self.lat = self.data.latitude.values
        lat_1 = self.data.latitude_1.values
        self.lat_b = np.append(lat_1, 2 * lat_1[-1] - lat_1[-2])
    
    def total_evap(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None, mode_t=None,
                   value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.total_evap.isel(surface=0).drop("surface")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class ICECONCMTS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(ICECONCMTS, self).__init__(experiment, start_year, end_year, file_name="iceconc.monthly",
                                         month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(ICECONCMTS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def iceconc(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None, mode_t=None,
                value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.iceconc_mm_srf.isel(surface=0).drop("surface")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class ICEDEPTHMTS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(ICEDEPTHMTS, self).__init__(experiment, start_year, end_year, file_name="icedepth.monthly",
                                          month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(ICEDEPTHMTS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def icedepth(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None, mode_t=None,
                 value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.icedepth_mm_srf.isel(surface=0).drop("surface")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class LHMTS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(LHMTS, self).__init__(experiment, start_year, end_year, file_name="lh.monthly",
                                    month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(LHMTS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def lh(self, zone=zones.NoZone(), mode_lon=None, value_lon=None, mode_lat=None, value_lat=None, mode_t=None,
           value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.lh_mm_srf.isel(surface=0).drop("surface")
        return self.get(data_array, zone, mode_lon, value_lon, mode_lat, value_lat, None, None, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


class MERIDATS(HadCM3TS):
    
    def __init__(self, experiment, start_year, end_year, month_list=None, verbose=False, logger="print"):
        self.data = None
        super(MERIDATS, self).__init__(experiment, start_year, end_year, file_name="merid.annual",
                                       month_list=month_list, verbose=verbose, logger=logger)
    
    def import_coordinates(self):
        super(MERIDATS, self).import_coordinates()
        
        self.lon = self.data.longitude.values
        self.lon_b = util.guess_bounds(self.lon)
        
        self.lat = self.data.latitude.values
        self.lat_b = util.guess_bounds(self.lat)
    
    def atlantic(self, zone=zones.NoZone(), mode_lat=None, value_lat=None, mode_z=None, value_z=None, mode_t=None,
                 value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.Merid_Atlantic.rename({'depth': 'z'})
        return self.get(data_array, zone, None, None, mode_lat, value_lat, mode_z, value_z, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)
    
    def globalx(self, zone=zones.NoZone(), mode_lat=None, value_lat=None, mode_z=None, value_z=None, mode_t=None,
                value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.Merid_Global.rename({'depth': 'z'})
        return self.get(data_array, zone, None, None, mode_lat, value_lat, mode_z, value_z, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)
    
    def indian(self, zone=zones.NoZone(), mode_lat=None, value_lat=None, mode_z=None, value_z=None, mode_t=None,
               value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.Merid_Indian.rename({'depth': 'z'})
        return self.get(data_array, zone, None, None, mode_lat, value_lat, mode_z, value_z, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)
    
    def pacific(self, zone=zones.NoZone(), mode_lat=None, value_lat=None, mode_z=None, value_z=None, mode_t=None,
                value_t=None, new_start_year=None, new_end_year=None, new_month_list=None):
        data_array = self.data.Merid_Pacific.rename({'depth': 'z'})
        return self.get(data_array, zone, None, None, mode_lat, value_lat, mode_z, value_z, mode_t, value_t,
                        new_start_year=new_start_year, new_end_year=new_end_year, new_month_list=new_month_list)


# *************
# LAND-SEA MASK
# *************

class HadCM3LSM(proc.LSM):
    
    def __init__(self):
        super(HadCM3LSM, self).__init__()
    
    def get_lsm(self, lsm_name):
        ds_lsm = xr.open_dataset(util.path2lsm[lsm_name])
        self.lon = ds_lsm.longitude.values
        self.lat = ds_lsm.latitude.values
        self.depth = ds_lsm.depthdepth.values
        self.level = ds_lsm.depthlevel.values
        self.lsm2d = ds_lsm.lsm.values
        self.mask2d = (self.lsm2d - 1) * -1
    
    def fit_lsm_ds(self, ds):
        # Should check if longitudes are equal
        if self.depth is None:
            print("The lsm haven't been imported yet. Calling ls_from_ds instead")
            self.lsm_from_ds(ds)
        else:
            self.lon, self.lat, self.z = ds.longitude.values, ds.latitude.values, ds.depth.values
            lsm3d = np.zeros((len(self.lon), len(self.lat), len(self.z)))
            for i in range(len(self.z)):
                lsm3d[:, :, i] = np.ma.masked_less(self.depth, self.z[i])
            self.lsm3d = lsm3d
            self.mask3d = (lsm3d - 1) * -1
    
    def lsm_from_ds(self, ds):
        pass
