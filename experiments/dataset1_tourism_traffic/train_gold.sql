Select Sum(Area)  from lakes where name = '太湖'	ada
Select name from cities order by MbrMinY(Shape) asc limit 1	ada
Select distinct provinces.name from provinces inner join lakes On Intersects(provinces.Shape, lakes.Shape) = 1 where lakes.name = '洞庭湖'	ada
Select distinct provinces.name from rivers inner join provinces On Intersects(provinces.Shape, rivers.Shape) = 1 where rivers.name = '长江'	ada
Select Sum(GLength(Intersection(provinces.Shape, rivers.Shape), 1))  from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where provinces.name = '湖北省' and rivers.name = '长江'	ada
Select distinct rivers.name from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where provinces.name = '湖北省' and rivers.level_river = 1	ada
Select provinces.name, Sum(GLength(Intersection(provinces.Shape, rivers.Shape), 1))  from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 group by provinces.name	ada
Select name, Area(Shape, 1) as area from provinces order by area desc limit 1	ada
select province, count(*) from cities group by province	ada
Select b.name , Area(b.Shape, 1) from provinces a inner join provinces b On Touches(a.Shape, b.Shape) = 1 where a.name = '广东省'	ada
Select Sum(Shape_Length) from rails	ada
Select Sum(Shape_Length) from rails where name = '京广线'	ada
Select distinct cities.name from cities inner join rails On Intersects(cities.Shape, rails.Shape) = 1 where cities.province = '河南省' and rails.name = '京广线'	ada
Select distinct cities.name from cities inner join rails On Intersects(cities.Shape, rails.Shape) = 1	ada
Select name from cities where name not in (Select distinct cities.name from cities inner join rails On Intersects(cities.Shape, rails.Shape) = 1 )	ada
Select name, Area(Shape, 1)   from provinces where name = (Select name from provinces order by POPU desc limit 1)	ada
Select Sum(Area)  from lakes where level_lake = 1	ada
Select name from provinces order by GDP_2000 - GDP_1994 desc limit 1	ada
Select name, Area(Shape, 1)   from provinces where name = (Select name from provinces order by Pop_Minori desc limit 1)	ada
Select distinct rivers.name from rivers inner join rails On Intersects(rivers.Shape, rails.Shape) = 1 where rivers.level_river = 1	ada
Select airports.name from provinces inner join airports On Within(airports.Location, provinces.Shape) = 1 where provinces.name = '湖北省'  order by Distance(Centroid(provinces.Shape), airports.Location, 1) asc limit 1	ada
Select distinct b.name from rails a inner join rails b On Intersects(a.Shape, b.Shape) = 1 where a.name = '盘西' and b.name != '盘西'	ada
Select distinct rivers.name from rivers inner join provinces On Intersects(rivers.Shape, provinces.Shape) =1 where provinces.name = '新疆维吾尔自治区'	ada
Select Sum(GLength(Intersection(rivers.Shape, provinces.Shape), 1))  from rivers inner join provinces On Intersects(rivers.Shape, provinces.Shape) =1 where provinces.name = '新疆维吾尔自治区'	ada
Select Sum(Area(Shape,1))  , Sum(POPU) from provinces where name like '%自治区'	ada
Select name, POPU from provinces where name like '%自治区' and name = ( Select name from provinces where name like '%自治区' order by Area(Shape, 1) asc limit 1)	ada
Select distinct provinces.name from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where rivers.name = '长江'  intersect  Select distinct provinces.name from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where rivers.name = '黄河'	ada
Select Sum(Pop_65Plus) from provinces where name in (Select distinct provinces.name from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where rivers.name = '长江')	ada
Select distinct rails.name from rivers inner join rails On Intersects(rails.Shape, rivers.Shape) = 1 where rivers.name = '长江'	ada
Select Sum(Area(provinces.Shape, 1))   from provinces where name in (Select distinct provinces.name from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where rivers.name = '长江')	ada
Select name, Pop_Urban from provinces where name in (Select distinct provinces.name from provinces inner join rails On Intersects(provinces.Shape, rails.Shape) = 1 where rails.name = '京广线')	ada
Select name from cities order by MbrMinX(Shape) asc limit 1	ada
Select name from provinces order by MbrMaxX(Shape) desc limit 1	ada
Select provinces.name, Sum(GLength(Intersection(provinces.Shape, rivers.Shape), 1))  from provinces inner join rivers On Intersects(provinces.Shape, rivers.Shape) = 1 where level_river = 1 group by provinces.name	ada
Select provinces.name, count(*) from provinces inner join airports On Within(Location, Shape) = 1 group by provinces.name	ada
Select cities.name from cities inner join airports On Distance(Shape, Location, 1) < 200 * 1000 where airports.name = '安庆'	ada
Select count(*) from provinces inner join airports On Within(Location, Shape) = 1 where provinces.name in ('北京市', '河北省', '天津市')	ada
Select airports.name, min(Distance(cities.Shape, airports.Location, 1))  as distance from cities inner join airports where cities.name = '苏州市' order by distance limit 1	ada
Select provinces.name, count(*) from provinces inner join airports On Contains(provinces.Shape, airports.Location) = 1 where provinces.name = (Select name from provinces order by POPU desc limit 1)	ada
Select distinct airports.name from airports inner join rails On Distance(airports.Location, rails.Shape, 1) < 10 * 1000 where rails.name = '京广线'	ada
Select airports.name from airports inner join provinces On Within(airports.Location, provinces.Shape) = 1 inner join lakes where provinces.name = '江苏省' and lakes.name = '太湖' order by Distance(airports.Location, lakes.Shape, 1) asc limit 1	ada
Select name, Area(Shape, 1)   from provinces order by Pop_Female desc limit 1	ada
Select cities.name, count(*) as count from cities inner join airports On Within(airports.Location, cities.Shape) = 1 group by cities.name order by count desc limit 1	ada
Select name, Sum(Shape_Length) as length  from rails group by name order by length desc limit 1	ada
Select provinces.name, count(*) from provinces inner join airports On Contains(provinces.Shape, airports.Location) =1 where provinces.name = (Select name from provinces order by abs(Pop_Male - Pop_Female) desc limit 1)	ada
Select distinct airports.name from lakes inner join airports On Distance(lakes.Shape, airports.Location, 1) < 200 * 1000 where lakes.name = '太湖'	ada
Select name from cities where province = '吉林省' order by MbrMaxY(Shape) desc limit 1	ada
Select distinct cities.name from rails inner join cities On Intersects(rails.Shape, cities.Shape) = 1 where rails.name = '湘桂线'	ada
Select GLength(Intersection(a.Shape, b.Shape),1)  from provinces a inner join provinces b On Intersects(a.Shape, b.Shape) = 1 where a.name = '河南省' and b.name = '湖北省'	ada
Select cities.name from provinces inner join cities On Within(Centroid(provinces.Shape), cities.Shape) = 1 where provinces.name = '湖北省'	ada
Select b.name, GLength(Intersection(a.Shape, b.Shape),1)  from provinces a inner join provinces b On Intersects(a.Shape, b.Shape) = 1 where a.name = '河南省'	ada
Select airports.name, Distance(airports.Location, Intersection(a.Shape, b.Shape), 1)  as d from provinces a inner join provinces b On a.name = '河南省' and b.name = '湖北省' and Intersects(a.Shape, b.Shape) = 1  inner join airports order by d asc limit 1	ada
Select name from provinces where  Within(Centroid(Shape), Shape) = 0	ada
Select name, Sum(length) from rivers where name in ('长江', '黄河') group by name	ada
Select province, count(*) from cities group by province order by count(*) desc limit 1	ada
Select distinct provinces.name from provinces inner join (Select Intersection(rails.Shape, rivers.Shape) as Location from rails inner join rivers On Intersects(rails.Shape, rivers.Shape) = 1 where rails.name = '京广线' and rivers.name = '黄河') As Inters On Within(Location, Shape) = 1	ada
Select count(*) from universities where province = '北京市'	edu
Select province, count(*) from universities group by province	edu
Select name, Shape_Area from cities where province = '河北省'	edu
Select b.name from provinces a inner join provinces b on Touches(a.Shape, b.Shape) = 1 where a.name = '北京市'	edu
Select province, count(*) from universities where province in (Select b.name from provinces a inner join provinces b on Touches(a.Shape, b.Shape) = 1 where a.name = '北京市') group by province	edu
Select Area(Shape, 1) from provinces where name = '湖北省'	edu
Select Sum(POP2020) from cities where province = '湖北省'	edu
Select name from universities where project_211 = 1 order by X(Location) asc limit 1	edu
Select (Sum(POP2020) - Sum(POP2000)) from cities where province = '湖北省'	edu
Select  name from universities where province = '湖北省' and (universities.project_211 = 1 or universities.project_985 = 1)	edu
Select name from cities where province = '湖北省' order by Shape_Area desc limit 1	edu
Select name, Shape_Area from cities where province = '内蒙古自治区'	edu
Select province, count(*) from universities where project_211 = 1 or project_985 = 1 group by province	edu
Select Sum(Shape_Area) from cities where province in ('北京市', '天津市', '河北省')	edu
Select name from provinces order by MbrMinX(Shape) asc limit 1	edu
Select Distance(Centroid(provinces.Shape), Centroid(cities.Shape), 1)  from provinces inner join cities where provinces.name = '河南省' and cities.name = '郑州市'	edu
Select b.name from cities a inner join cities b on Touches(a.Shape, b.Shape) = 1 where a.name = '安阳市' and b.province != '河南省'	edu
Select name, Area(Shape, 1) from cities where name = (Select name from cities where administrative_division_category != '直辖市'  order by POP2020 desc limit 1)	edu
Select a.name from universities a inner join universities b on Distance(a.Location, b.Location, 1) < 3000 where a.project_985 = 1 and b.name = '北京大学' and a.name != '北京大学'	edu
Select Sum(POP2020) from provinces inner join cities on Contains(provinces.Shape, cities.Shape) = 1 where provinces.name = '北京市' or provinces.name = '天津市' or provinces.name = '河北省'	edu
Select name, POP2020 from cities where province = '内蒙古自治区'	edu
Select name from provinces where name not in (Select distinct province from universities where project_985 = 1)	edu
Select distinct city from universities where project_211 = 1 or project_985 = 1	edu
Select distinct city from universities where project_211 = 1 and project_985 = 1	edu
Select name from cities where name not in (Select distinct cities.name from cities inner join universities on universities.city = cities.name where universities.project_985 = 1) and administrative_division_category = '地级市'	edu
Select name from provinces where name not in (Select distinct a.name from provinces a inner join provinces b on Touches(a.Shape, b.Shape) = 1 where a.name != b.name)	edu
Select a.name, count(*) from provinces a inner join provinces b on Touches(a.Shape, b.Shape) = 1 where a.name != b.name group by a.Name	edu
Select b.name,  Distance(a.Location, b.Location, 1) from universities a inner join universities b where a.name = '北京大学' and b.province = '北京市' and b.name != '北京大学' order by Distance(a.Location, b.Location, 1) asc limit 1	edu
Select b.name,  Distance(a.Location, b.Location, 1) from universities a inner join universities b where a.name = '北京大学' and b.province = '北京市' and b.name != '北京大学' and (b.project_211 = 1 or b.project_985 = 1) order by Distance(a.Location, b.Location, 1) asc limit 5	edu
Select count(*) from universities where province = '湖北省' and affiliation = '教育部'	edu
Select cities.name from provinces inner join cities on Contains(provinces.Shape, cities.Shape) = 1 where provinces.name = '河南省' and cities.name not in (Select distinct b.name from provinces a inner join cities b on Contains(a.Shape, b.Shape) = 1 inner join provinces c on Intersects(b.Shape,  c.Shape) = 1  where a.name = '河南省' and c.name != '河南省')	edu
Select distinct cities.name from cities inner join provinces On Intersects(cities.Shape, provinces.Shape) = 1 where cities.province = '河南省' and provinces.name != '河南省'	edu
select b.name from cities a inner join cities b on Touches(a.Shape, b.Shape) = 1 where a.name = '郑州市' order by b.POP2020 desc limit 1	edu
Select distinct SRID(Location) from universities	edu
Select province, count(*) from universities where operation_type = '民办' group by province	edu
Select count(*) from universities where province = '河北省' and name like '%职业%'	edu
Select distinct province from universities where name like '中国%'	edu
Select province, name from universities where name like '中国%'	edu
Select name from cities where province = '河北省' order by POP2020 desc limit 1	edu
Select name , POP2020 from cities where province = '湖北省' order by Area(Shape, 1) desc limit 1	edu
Select city, count(*) from universities where city = (Select cities.name from provinces inner join cities on Contains(provinces.Shape, cities.Shape) = 1 where provinces.name = '湖北省' order by Area(cities.Shape, 1) desc limit 1)	edu
Select city, count(*) from universities where province = '江苏省' and (project_211 = 1 or project_985 = 1) group by city order by count(*) desc limit 1	edu
Select (Select Area(Shape, 1) from provinces where name = '内蒙古自治区') - (Select Area(Shape, 1) from provinces where name = '河北省')	edu
Select province, count(*) from universities where affiliation = '国家民委' group by province	edu
