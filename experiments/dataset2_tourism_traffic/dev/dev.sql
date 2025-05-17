Select Sum(Domestic_Tourism_Earnings_Wan_Yuan) from tours inner join cities On cities.name = tours.city and cities.province in ('辽宁省', '吉林省', '黑龙江省') where tours.year = 2020	tourism
Select Sum(international_toursim_earnings_Wan_dollar) from cities inner join tours On cities.name = tours.city and cities.province = '湖北省' where tours.year = 2020	tourism
Select Sum(star_hotel_number) from cities inner join tours on cities.name = tours.city where year = 2010 and cities.province = '湖北省'	tourism
Select cities.name, count(*) from cities inner join airports On Contains(cities.Shape, airports.Location) = 1 group by cities.name	tourism
Select name from cities where name not in (Select distinct cities.name from cities inner join airports On Contains(cities.Shape, airports.Location) = 1)	tourism
Select cities.name, count(*) from ScenicSpots inner join cities On Within(ScenicSpots.Location, cities.Shape) = 1 where ScenicSpots.level = '5A' group by cities.name	tourism
Select province, Sum(Area(Shape, 1)) from cities group by province	tourism
Select province, Sum(Area(Shape, 1)) as area from cities group by province order by area desc limit 1	tourism
Select province from cities order by MbrMinX(Shape) asc limit 1	tourism
Select province from cities order by MbrMinY(Shape) asc limit 1	tourism
Select name from cities where province = '河南省' order by MbrMaxY(Shape) desc limit 1	tourism
Select count (*) from stations inner join ScenicSpots On Distance(stations.Location, ScenicSpots.Location, 1) < 10 * 1000 where stations.name = '六安' and ScenicSpots.level > '3A'	tourism
Select ScenicSpots.name,  Distance(stations.Location, ScenicSpots.Location, 1) from stations inner join ScenicSpots On Distance(stations.Location, ScenicSpots.Location, 1) < 100 * 1000 where stations.name = '岳阳东' and ScenicSpots.level = '5A'	tourism
Select cities.province, count(*) from cities inner join airports On Contains(cities.Shape, airports.Location) = 1 where cities.province = (Select province from GDPs order by year_2023 desc limit 1)	tourism
Select province from GDPs order by year_2023 desc limit 1	tourism
Select city from tours where year >= 2011 and year <= 2020 group by city order by Sum(international_tourists_number_Wan) desc limit 1	tourism
Select count(*) from cities inner join airports On Within(airports.Location, cities.Shape) = 1 where cities.name = '哈尔滨市'	tourism
Select airports.name from cities inner join airports On Within(airports.Location, cities.Shape) = 1 where cities.name = '北京市'	tourism
Select count(*) from cities inner join ScenicSpots On Within(ScenicSpots.Location, cities.Shape) = 1 where cities.province = '新疆维吾尔自治区'  and ScenicSpots.level >= '3A'	tourism
Select Sum(Area(Shape, 1)) from cities where province = '西藏自治区'	tourism
Select Sum(international_toursim_earnings_Wan_dollar) from tours inner join cities On cities.name = tours.city and cities.province in ('辽宁省', '吉林省', '黑龙江省') where tours.year = 2020	tourism
Select Sum(Area(Shape, 1)) from cities where province in ('辽宁省', '吉林省', '黑龙江省')	tourism
Select province, Sum(Area(Shape, 1)) from cities where province in ('辽宁省', '吉林省', '黑龙江省') group by province order by Sum(Area(Shape, 1)) desc limit 1	tourism
Select count(distinct cities.name) from cities inner join airports On Distance(airports.Location, cities.Shape, 1) < 150 * 1000 where airports.name = '大理'	tourism
Select ScenicSpots.name, Distance(Centroid(cities.Shape), ScenicSpots.Location, 1) as d from cities inner join ScenicSpots where Contains(cities.Shape, ScenicSpots.Location) =  1 and cities.name = '北京市' and ScenicSpots.level = '5A' order by d desc limit 1	tourism
Select Distance(a.Location, b.Location, 1)  from ScenicSpots a inner join ScenicSpots b where a.name = '北海公园' and b.name = '恭王府'	tourism
Select b.name, Distance(a.Location, b.Location, 1) from ScenicSpots a inner join ScenicSpots b where a.name = '八大处公园' and b.level = '5A' and b.name != a.name order by Distance(a.Location, b.Location, 1)   asc limit 1	tourism
Select cities.name from cities inner join airports on Within(airports.Location, cities.Shape) = 1 where airports.name = '阿克苏/温宿'	tourism
Select cities.name  from cities inner join ScenicSpots On Contains(cities.Shape, ScenicSpots.Location) = 1 where ScenicSpots.name = '天台山景区'	tourism
Select cities.name, count(*) from cities inner join ScenicSpots On Contains(cities.Shape, ScenicSpots.Location) = 1 where cities.name in (Select city from tours where year = 2020 order by international_tourists_number_Wan  desc limit 10) and ScenicSpots.level = '5A' group by cities.name	tourism
Select cities.province, Sum(Domestic_Tourism_Earnings_Wan_Yuan) from tours inner join cities On cities.name = tours.city and cities.province in ('辽宁省', '吉林省', '黑龙江省') where tours.year = 2020 group by cities.province	tourism
Select province, Sum(Area(Shape, 1)) from cities where province in (Select b.province from GDPs a inner join GDPs b where a.province = '浙江省' and b.year_2023 > a.year_2023) group by province	tourism
Select city, star_hotel_number from tours where year = 2020 order by star_hotel_number desc limit 1	tourism
Select GLength(Shape, 1) from buslines where name = '874路'	traffic
Select name, GLength(Shape, 1) as distance from buslines order by distance desc limit 1	traffic
Select name, start_stop, end_stop, GLength(Shape, 1) as distance from buslines order by distance desc limit 10	traffic
Select name, Sum(GLength(Shape, 1)) from roads group by name	traffic
Select name, Sum(GLength(Shape, 1)) as length from roads group by name order by length desc  limit 1	traffic
Select Sum(Area(Shape,1)) from greenspaces	traffic
Select name, Sum(Area(Shape,1)) from greenspaces  group by name	traffic
Select name, Sum(Area(Shape,1))  as area  from greenspaces  group by name order by area desc limit 1	traffic
Select Sum(Area(Shape, 1)) from greenspaces where name = '玄武湖公园'	traffic
Select districts.name, Sum(Area(Intersection(districts.Shape, greenspaces.Shape), 1)) from districts inner join greenspaces where Intersects(districts.Shape, greenspaces.Shape) = 1 group by districts.name	traffic
Select districts.name, Sum(Area(Intersection(districts.Shape, greenspaces.Shape), 1)) as area from districts inner join greenspaces where Intersects(districts.Shape, greenspaces.Shape) = 1 group by districts.name order by area desc limit 1	traffic
Select line, count(*) from subwaystations group by line order by line	traffic
Select line, count(*) from subwaystations group by line	traffic
Select buslines.name from busstops inner join buslines where start_stop = busstops.name and start_time = '0500'	traffic
Select hotels.name, Distance(busstops.Location, hotels.Location, 1) as d from busstops inner join hotels on busstops.name = '三元巷' order by d asc limit 5	traffic
Select line, count(*) as count from subwaystations group by line order by count desc limit 1	traffic
Select distinct subways.line, count(*) from subways inner join districts on Intersects(subways.Shape, districts.Shape) = 1 group by subways.line	traffic
Select GLength(Shape, 1) from subways where line = 'line4'	traffic
Select distinct b.line from subways a inner join subways b on Intersects(a.Shape, b.Shape) = 1 where a.line = 'line10二期' and b.line != a.line	traffic
Select Sum(GLength(Shape, 1)) from subways	traffic
Select subwaystations.station,  Distance(agencies.Location, subwaystations.Location, 1) as distance from agencies inner join subwaystations where agencies.name = '南京市文物局' order by distance asc limit 1	traffic
Select hotels.name, Distance(subwaystations.Location, hotels.Location, 1) from subwaystations inner join hotels on Distance(subwaystations.Location, hotels.Location, 1) < 1000 where subwaystations.station = '鼓楼' and subwaystations.line = 'line4'	traffic
Select subwaystations.station from buslines a inner join buslines b on a.name = '874路' and b.name = '711路' inner join subwaystations where Intersects(a.Shape, b.Shape) = 1 order by Distance(Intersection(a.Shape, b.Shape), subwaystations.Location, 1) asc limit 1	traffic
Select subwaystations.station, Distance(Intersection(a.Shape, b.Shape), subwaystations.Location, 1) as distance from roads a inner join roads b on a.name = '秦淮路' and b.name = '将军大道' inner join subwaystations where Intersects(a.Shape, b.Shape) = 1 order by distance asc limit 1	traffic
Select name, Sum(GLength(Shape, 1))  from rails group by name	traffic
Select name, Sum(GLength(Shape, 1)) as length from rails group by name order by length desc limit 1	traffic
Select Sum(GLength(Shape, 1)) from rails	traffic
Select districts.name, count(*) as count from districts inner join agencies on Contains(districts.Shape, agencies.Location) = 1 group by districts.name order by count desc limit 1	traffic
Select distinct districts.name from districts inner join subwaystations on Within(subwaystations.Location, districts.Shape) = 1 where subwaystations.station = '大行宫'	traffic
Select districts.name from districts inner join agencies on Within(agencies.Location, districts.Shape) = 1 where agencies.name = '江苏省海事局'	traffic
Select name, Area(Shape, 1) as area from districts order by area desc limit 1	traffic
Select districts.name, Area(Shape, 1) from districts	traffic
Select districts.name, count(*)  from districts inner join subways On Intersects(districts.Shape, subways.Shape) = 1 group by districts.name	traffic
Select distinct hotels.name from roads inner join hotels On Distance(roads.Shape, hotels.Location, 1) < 1000 where roads.name = '广州路'	traffic
Select subwaystations.station, Distance(subwaystations.Location, agencies.Location, 1) as d from subwaystations inner join agencies On agencies.name = '南京市房产局' order by d asc limit 1	traffic
Select count (*) from districts inner join subways On Intersects(districts.Shape, subways.Shape) = 1 where districts.name = '玄武区'	traffic
Select buslines.name from districts inner join busstops on Within(busstops.Location, districts.Shape) = 1 and districts.name = '六合区' inner join buslines where buslines.start_stop = busstops.name and buslines.start_time = '0500'	traffic
Select distinct districts.name, buslines.name from districts inner join busstops on Within(busstops.Location, districts.Shape) = 1 inner join buslines where buslines.start_stop = busstops.name and buslines.start_time < '0500'	traffic
Select subwaystations.station, Distance(subwaystations.Location, buslines.Shape, 1) as d from buslines inner join subwaystations On buslines.name = '709路' order by d asc limit 1	traffic
Select hotels.name, Distance(agencies.Location, hotels.Location, 1) as d from agencies inner join hotels On d < 500 where agencies.NAME = '南京市文物局' order by Distance(agencies.Location, hotels.Location, 1) asc limit 5	traffic
Select distinct buslines.name from buslines inner join roads On Intersects(buslines.Shape, roads.Shape) = 1 where roads.name = '建康路'	traffic
Select districts.name, count(*) as count from agencies inner join districts On Within(agencies.Location, districts.Shape) = 1 group by districts.name order by count desc limit 1	traffic
Select hotels.name, Distance(hotels.Location, subwaystations.Location, 1) as distance from hotels inner join districts on Within(hotels.Location, districts.Shape) = 1 and districts.name = '江宁区' inner join subwaystations on subwaystations.station = '南京南站' order by distance asc limit 1	traffic
Select districts.name, Sum(GLength(Intersection(districts.Shape, subways.Shape), 1)) from districts inner join subways On Intersects(districts.Shape, subways.Shape) = 1 group by districts.name	traffic
Select districts.name, Sum(GLength(Intersection(districts.Shape, subways.Shape), 1)) as length  from districts inner join subways On Intersects(districts.Shape, subways.Shape) = 1 group by districts.name order by length desc limit 1	traffic
Select subways.Line from districts inner join subways On Intersects(districts.Shape, subways.Shape) = 1 where districts.name = '玄武区'	traffic
Select distinct districts.name from rails inner join districts On Intersects(rails.Shape, districts.Shape) = 1	traffic
Select count(*) from districts inner join hotels On Contains(districts.Shape, hotels.Location) = 1 where districts.name = '玄武区'	traffic
Select count(distinct hotels.name) from subways inner join hotels On Distance(subways.Shape, hotels.Location, 1) < 500 where subways.line = 'S7'	traffic
Select distinct districts.name from districts inner join greenspaces On Intersects(greenspaces.Shape, districts.Shape) = 1 where greenspaces.name = '钟山风景区'	traffic
Select subwaystations.station, Distance(greenspaces.Shape, subwaystations.Location, 1) as distance from greenspaces inner join subwaystations On greenspaces.name = '郑和公园' order by distance asc limit 1	traffic
Select greenspaces.name from subwaystations inner join greenspaces on subwaystations.station = '上海路' where greenspaces.name like '%公园%' order by Distance(subwaystations.Location, greenspaces.Shape, 1) asc limit 1	traffic
Select Sum(Area(Shape, 1)) from rivers where name = '长江'	traffic
Select distinct subways.line from subways inner join rivers on Crosses(rivers.Shape, subways.Shape) = 1 where rivers.name = '长江'	traffic
Select distinct districts.name from rivers inner join districts On Intersects(rivers.Shape, districts.Shape) = 1 where rivers.name = '长江'	traffic
Select districts.name,  Sum(Area(Intersection(rivers.Shape, districts.Shape), 1)) from rivers inner join districts On Intersects(rivers.Shape, districts.Shape) = 1 where rivers.name = '长江' group by districts.name	traffic
Select distinct subwaystations.station from subwaystations inner join rivers On Distance(subwaystations.Location, rivers.Shape, 1) < 1000 where rivers.name = '长江'	traffic
Select buslines.name from buslines inner join rivers On Crosses(buslines.Shape, rivers.Shape) = 1 where rivers.name = '长江'	traffic
Select hotels.name from hotels inner join rivers On rivers.name = '长江' order by Distance(rivers.Shape, hotels.Location, 1) asc limit 1	traffic
Select hotels.name, Distance(agencies.Location, hotels.Location, 1) as distance from agencies inner join hotels On agencies.name = '高淳县教育局委员会' order by distance asc limit 1	traffic
Select greenspaces.name, Distance(subways.Shape, greenspaces.Shape, 1) as distance from subways inner join greenspaces On subways.line = 'line1' where greenspaces.name like '%公园%' order by distance asc limit 1	traffic
Select districts.name, count(*) from subwaystations inner join districts On Within(subwaystations.Location, districts.Shape) = 1 group by districts.name	traffic
Select districts.name, count(*) as count from subwaystations inner join districts On Within(subwaystations.Location, districts.Shape) = 1 group by districts.name order by count desc limit 1	traffic
Select Line, GLength(Shape, 1) as length from subways order by length desc limit 1	traffic
Select distinct b.Name from roads a inner join roads b On Intersects(a.Shape, b.Shape) = 1 where a.Name = '东风路' and a.Name != b.Name	traffic
Select subwaystations.station, Distance(subwaystations.Location, hotels.Location, 1) as d from subwaystations inner join hotels where hotels.name = '金龙大酒店' order by d asc limit 1	traffic
Select name, Area(Shape, 1) from districts where name in ('玄武区', '秦淮区')	traffic
