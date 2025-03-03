import os
import matplotlib.pyplot as plt
import matplotlib
from shapely.geometry import MultiPolygon, GeometryCollection, LineString, Point
from matplotlib.lines import Line2D
from l26_geometry_reader.discretizer import Discretizer
from shapely.geometry import Polygon
from shapely.validation import make_valid
from my_function.backend.services.lst_service import LstRequestService
from io import BytesIO

class GeoPlot:
    def __init__(self):
        self.img = None
        self.geo_json = None
    
    def _get_bending_lines(self,geo_in):
        bending_lines = []
        for bending in geo_in.get('bendings', []):
            lines = bending.get('bending_lines', [])
            for line in lines:
                bending_lines.append(self._linestring_from_dict(line))
        return bending_lines  


    def _discretize_part_to_polygon(self,part):
        outer_contour, inner_contours = Discretizer.discretize_geometry(part, arc_delta_u=0.5)  
        inner_contours = [e for e in inner_contours if len(e.flatten()) >= 6]
        return make_valid(Polygon(outer_contour, inner_contours))  


    def _linestring_from_dict(self,d):
        Point1 = Point(d['start_point']['x'], d['start_point']['y'])
        Point2 = Point(d['end_point']['x'], d['end_point']['y'])
        return LineString([Point1, Point2])


    def _add2plot(self,poly_in):
        
        if isinstance(poly_in, list):
            for p in poly_in:
                self._add2plot(p)
        if isinstance(poly_in, MultiPolygon) or isinstance(poly_in, GeometryCollection):
            for geom in poly_in.geoms:
                self._add2plot(geom)
        if isinstance(poly_in, Polygon):
            x, y = poly_in.exterior.xy
            plt.plot(x, y)
            for interior in poly_in.interiors:
                x_i, y_i = interior.xy
                plt.plot(x_i, y_i)


    def _plot_polygon(self, poly_in, lines=None):
        
        self._add2plot(poly_in)

        if lines:
            if isinstance(lines, LineString):
                lines = list(lines)
            for line in lines:
                if not isinstance(line, LineString):
                    continue
                x = line.xy[0]
                y = line.xy[1]
                plt.gca().add_line(Line2D(x, y, lw=0.5, color='c'))

        self.img = BytesIO()
        plt.savefig(self.img, format='png', bbox_inches='tight', dpi=300)
        plt.close()
        self.img.seek(0)
        return self.img.getvalue()

    def _plot_geo(self,geo_json)->str:
        part_polygon = self._discretize_part_to_polygon(geo_json)
        bending_lines = self._get_bending_lines(geo_json)
        image_bytes = self._plot_polygon(part_polygon, lines=bending_lines)
        return image_bytes
    

    def create_geo_image(self,file_data:bytes, file_name:str, lst_service:LstRequestService, data_folder:str):
        matplotlib.use('Agg')
        file_path = os.path.join(data_folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        self.geo_json = lst_service.parse_geo_file(file_name,file_path)
        image_bytes = self._plot_geo(self.geo_json)
        os.remove(file_path)
        return image_bytes