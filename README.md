# Data_Visualisation

`input req for the http://127.0.0.1:5000/visualization_api/donut:`

 {"payload":{"chart_properties":{"explode":[0, 0, 0.2, 0, 0,0,0,0],"show_percentage":"Y","show_labels":"Y","show_legends":"Y","title":"Secured Loan","center_value":"14.20\n Cr"},"chart_value":{"data":[100,50,30,50,100,233,50,111],"label":["Jan","Feb","Mar","Apr","May","June", "July", "Aug"],"legend":["HL","PL","LAP","GL","AB","aa", "bb", "cc"]}}}

`input req for http://127.0.0.1:5000/visualization_api/line_and_bar`

{"chart_properties":{"plot_type":"line_graph","x_label":"MONTH","y_label":"AMOUNT","legend":["Logins"],"grid_line_show":"Y","hide_axis_line":["top","right"]},"chart_value":{"X":["Jan","Feb","Mar","Apr","May","Jun"],"Y":[20000000,10000000,20000000,30000000,35000000,40000000]}}

`input request for http://127.0.0.1:5000/visualization_api/multi_bars`

{"super_title":"Ecosystem Availability Insight","payload":[{"x":["Today","Yesterday","Last\nThursday","Last 7 Days\n(avg)"],"y":[6.1,3.1,0.5,1.7],"bar_color":["#C34A2C","#C34A2C","#4E9258","#FFBF00"],"x_label":"","y_label":"Values in %","title":"Third Party Rest/Soap APIs","remarks":{"#4E9258":"Below 1%","#FFBF00":"1% To 3%","#C34A2C":"Above 3%"}},{"x":["Today","Yesterday","Last\nThursday","Last 7 Days\n(avg)"],"y":[0.1,0.1,"NA","null"],"bar_color":["#4E9258","#4E9258","#4E9258","#4E9258"],"x_label":"","y_label":"Values in %","title":"Database APIs","remarks":{"#4E9258":"Below 1%","#FFBF00":"1% To 3%","#C34A2C":"Above 3%"}},{"x":["Today","Yesterday","Last\nThursday","Last 7 Days\n(avg)"],"y":[1,2.9,"NA","NA"],"bar_color":["#4E9258","#FFBF00","#4E9258","#4E9258"],"x_label":"","y_label":"Values in %","title":"Document Manager","remarks":{"#4E9258":"Below 1%","#FFBF00":"1% To 3%","#C34A2C":"Above 3%"}},{"x":["Today","Yesterday","Last\nThursday","Last 7 Days\n(avg)"],"y":["NA",100,60,74],"bar_color":["#4E9258","#C34A2C","#C34A2C","#C34A2C"],"x_label":"","y_label":"Values in %","title":"VahanaHub APIs","remarks":{"#4E9258":"Below 1%","#FFBF00":"1% To 3%","#C34A2C":"Above 3%"}},{"x":["Today","Yesterday","Last\nThursday","Last 7 Days\n(avg)"],"y":["NA",0.4,1.4,4.6],"bar_color":["#4E9258","#4E9258","#FFBF00","#C34A2C"],"x_label":"","y_label":"Values in %","title":"Custom APIs","remarks":{"#4E9258":"Below 1%","#FFBF00":"1% To 3%","#C34A2C":"Above 3%"}}]}


`input request for http://127.0.0.1:5000/visualization_api/single_bar`

- this bar graph is with the bench mark

{"payload":{"Mon":1.6,"Tue":0.9,"Wed":4.7,"Thu":2.5,"Fri":0.2,"Sat":3.3,"Sun":0.3},"properties":{"x_label":"Days","y_label":"Values in %","title":"Ecosystem Availability Insight","subtitle":"Third Party Rest/Soap APIs","hide_axis":["top","right"]}}
