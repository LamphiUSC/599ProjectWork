There are 4 major sub-folders in the Assignment. 
1. aggregate_scripts
2. 10visualizations
3. elasticsearch_visualization
4. image_space


The main input file containing the ufo data is :- 
ufo_awesome_FINAL_OUTPUT_v2.tsv

The intermediate files are as following:-


The main modified output file containing the ufo data is :- 



The libraries used/need to be installed are:-
brew install elasticsearch
pip3 install elasticsearch

The important files present in the folders are :-


The order in which the programs need to be executed:

IMAGE_SPACE:
1) image_space/flann_index/get.py
Moved the run() function out from flann_index.py to get.py as I didn't want the flann_index code to run everytime when the call is made to image similarity server.
Had to load the image_map and image_files pickle data which contained the precomputed flann_index.
Ran flann_index.py once to precompute the index.

2) image_space/flann_index/flann_index.py
In below OpenCV function call, tried different comparison methods. Has commented all but one.
dist = cv2.compareHist(hist, image_map[file], cv2.cv.CV_COMP_INTERSECT)

3) image_space/imagespace_flann/server/flann_imagecontentsearch.py
Did following changes to the file. Removed the query? string and the 'k' paramter from the GET request sent to image similarity server.
The value of k is hardcoded as 10 in the run() function.

#return requests.get(setting.get('IMAGE_SPACE_FLANN_INDEX') +'?query=' + params['histogram'] +'&k=' + str(limit)).json()
return requests.get(setting.get('IMAGE_SPACE_FLANN_INDEX') +params['histogram']).json()

4) image_space/imagespace/server/imagefeatures_rest.py
Did following chnages to this file.
a) Enabled the opencv logic by commenting the "cv2_available = False" statement
   cv2_available = False
   #cv2_available = False

b) Changed the flag as sown below as it is not available in OpenCV3.
   image = cv2.imdecode(file_bytes, flags=cv2.CV_LOAD_IMAGE_UNCHANGED)  #----> Original code
   image = cv2.imdecode(file_bytes, flags=cv2.IMREAD_COLOR)  #----> Changes


Environment variables setup in .bashrc

export OODT_HOME=~/Ass3/deploy/ 
export GANGLIA_URL=http://zipper.jpl.nasa.gov/ganglia/
export FILEMGR_URL=http://localhost:9000
export WORKFLOW_URL=http://localhost:9001
export RESMGR_URL=http://localhost:9002
export WORKFLOW_HOME=$OODT_HOME/workflow
export FILEMGR_HOME=$OODT_HOME/filemgr
export PGE_ROOT=$OODT_HOME/pge
export PCS_HOME=$OODT_HOME/pcs
export FMPROD_HOME=$OODT_HOME/tomcat/webapps/fmprod/WEB-INF/classes/

#URL to SOLR index
export IMAGE_SPACE_SOLR=http://localhost:8081/solr/imagecatdev/

#Directory containing all the image files.
export IMAGE_SPACE_SOLR_PREFIX=/home/aashish/mywork/images2/

# Apache webserver with root directory pointed to directory containing all the files.
export IMAGE_SPACE_PREFIX=http://localhost:80/

# This contains the filename of the file which contains list of all images with qualified path.
export IMAGE_SPACE_LISTS=/home/aashish/listings.txt

#Tangelo server URL and the corresponding get service which serves as the entry point for webservice call.
export IMAGE_SPACE_FLANN_INDEX=http://localhost:9220/get/



VISUALIZATIONS:
1) All 10 py scripts in aggregate_scripts
The generate the TSV files corresponding to the 10 aggregate data we have decided to visualize using D3:
	a) duration_year_count
	b) location_aggregation_cloud
	c) meteors_rural_vs_urban_year_count
	d) Population_dense_sparse_year_count
	e) ReportedBy_Male_Female_Adult_kid_year_count
	f) rural_vs_urban_year_count
	g) sci_fi_movies_vs_sighting
	h) ShapeReported_year_count
	i) UFOSightings_year_count
	j) Within_25Miles_Otherwise_year_count

2) Under 10 visualizations:
	a) -- Run dense_sparse_count/tsv_to_json.py to generate population.json from Population_dense_sparse_year_count.tsv
	   -- Run dense_sparse_count/3D_Donut.html to draw 2 Donut charts in Firefox
	b) -- Run duration_year_count/duration_plot.html to draw line chart in Firefox
	c) -- Run location_count/tsv_to_csv.py to generate location_aggregation_cloud.csv from location_aggregation_cloud.tsv
	   -- Run location_count/bubble_chart.html in Firefox
	d) -- Run meteorites_rural_urban_year_count/tsv_to_csv.py to generate test.csv from meteors_rural_vs_urban_year_count.tsv
	   -- Run meteorites_rural_urban_year_count/rural_urban_meteorite_count.html to draw multi-bar chart in Firefox
	e) -- Run Reported_By_Count/pie_chart.py to generate the total count of Male, Female, Adult and Kid in ReportedBy_Male_Female_Adult_kid_year_count_total.csv from ReportedBy_Male_Female_Adult_kid_year_count.tsv
	   -- Run Reported_By_Count/pie_chart.html in Firefox
	f) -- Run rural_urban_count/percent_rural_urban.py to generate percentage of urban population over rural population in data.json from rural_vs_urban_year_count.tsv
	   -- Run rural_urban_count/gauge.html to draw individual gauge charts for every year in Firefox
	g) -- Run sci_fi_count/sci_fi_count_dual_bar_charts.html to draw dual bar chart in Firefox
	h) -- Run shape_report_count/tsv_to_csv.py to generate ShapeReported_year_count.csv from ShapeReported_year_count.tsv
	   -- Run shape_report_count/grouped_bar_chart.html to draw multi-bar chart in Firefox
	i) -- Run sci_fi_count/UFO_Sightings_line_chart.html to draw line chart in Firefox
	j) -- Run Within_25_miles_count/neg_barchart_data.py to get all values for Within_25miles as positive values and for Outside_25_miles as negative values in data.tsv from Within_25Miles_Otherwise_year_count.tsv
	   -- Run Within_25_miles_count/negative_bar.html to draw negative-bar chart in Firefox

3) Under elasticsearch_visualization:
	b) Modify the config file under /usr/local/etc/elasticsearch/elasticsearch.yml to enable CORS
		http.cors.enabled: true
		http.cors.allow-origin: "/.*/"
		http.cors.allow-credentials: true
		http.cors.allow-methods : OPTIONS, HEAD, GET, POST, PUT, DELETE
		http.cors.allow-headers : "X-Requested-With,X-Auth-Token,Content-Type, Content-Length, Authorization"
	c) Start elasticsearch server using brew services start elasticsearch
	d) Run TSV_To_JSON_ES.py to index elasticsearch with index data from ufo_awesome_FINAL_OUTPUT_v2.tsv under "bigdata"
	e) Run world_map_ES.html. Select a year and world map with black dots indicating location will be plotted.

	Environment variables setup in .bashrc
		export ES_HOME=~/apps/elasticsearch/elasticsearch-6.4.2
		export JAVA_HOME=$(/usr/libexec/java_home)
		export PATH=$ES_HOME/bin:$JAVA_HOME/bin:$PATH






