// 绘制线性图表,chartid(HTML中canvas标签的名字),labelname(图表的名称,例如CPU利用率)
// labels(X轴刻度的标签名字),datas(Y轴刻度的值),colors(颜色)
function chart_line(chartid, labelname, labels, datas, colors){
        chart = document.getElementById(chartid);//找到HTML中id为chartid的标签
        chartData = {
                    labels: labels,//labels(X轴刻度的标签名字)
                    datasets: [
                                {
                                    data: datas,//datas(Y轴刻度的值)
                                    label : labelname,//labelname(图表的名称,例如CPU利用率)
                                    backgroundColor: 'transparent',//透明线
                                    borderColor: colors[0],//线的颜色
                                    borderWidth: 1,//线的粗度
                                    pointBackgroundColor: colors[1]//线上点的颜色
                                },
                              ]
                    };
        if (chart) {//如果找到HTML中id为chartid的标签
                    new Chart(chart, { //在这个chart的位置绘制新的图表
                        type: 'line',//线形图
                        data: chartData,//使用上面设置的数据和参数
                        options: {
                                    scales: {
                                                yAxes: [
                                                        {
                                                            ticks: {
                                                                    beginAtZero: false//y轴可以不从0开始计数
                                                                    }
                                                        }
                                                        ]
                                            },
                                    legend: {
                                        display: true//显示labelname(图表的名称,例如CPU利用率)
                                            }
                                  }
                                    }
                            );
                    }
    }

// 绘制柱状图表,chartid(HTML中canvas标签的名字),labelname(图表的名称,例如CPU利用率)
// labels(X轴刻度的标签名字),datas(Y轴刻度的值),colors(颜色)
function chart_bar(chartid, labelname, labels, datas, colors){
        chart = document.getElementById(chartid);//找到HTML中id为chartid的标签
        chartData = {
                    labels: labels,// labels(X轴刻度的标签名字)
                    datasets: [
                                {
                                data: datas,//datas(Y轴刻度的值)
                                label : labelname,//labelname(图表的名称,例如CPU利用率)
                                backgroundColor: colors[0]//柱状图每一个柱的背景颜色,如果不使用[0],会造成每一个柱不同颜色
                                },
                               ]
                    };
        if (chart) {//如果找到HTML中id为chartid的标签
                    new Chart(chart, {//在这个chart的位置绘制新的图表
                                        type: 'bar',//柱状图
                                        data: chartData,//使用上面设置的数据和参数
                                        options: {
                                                    scales: {
                                                                xAxes: [{   //两个占比和为分母
                                                                            barPercentage: 0.2,//柱占比(越小越细)
                                                                            categoryPercentage: 0.8//归类占比
                                                                        }],
                                                                yAxes: [{
                                                                            ticks: {
                                                                                    beginAtZero: false//y轴可以不从0开始计数
                                                                                    }
                                                                        }]
                                                            },
                                                    legend: {
                                                        display: true//显示labelname(图表的名称,例如CPU利用率)
                                                            }
                                                  }
                                      }
                              );
                    }
    }

// 绘制饼状图表,chartid(HTML中canvas标签的名字),
// labels(每一个扇面的标签名字),datas(每一个扇面的数值),colors(颜色)
function chart_pie(chartid, labels, datas, colors){
    let donutOptions = {
                        cutoutPercentage: 50,//饼状图的粗细,如果是100,就什么也看不到了,0就是一个完整的饼
                        //标签注释出现的位置position: 'bottom',labels设置了标签的样式
                        legend: {position: 'bottom', padding: 5, labels: {pointStyle: 'circle', usePointStyle: true}}
                        };

    let chDonutData = {
                        labels: labels,// labels(每一个扇面的标签名字)
                        datasets: [
                                    {
                                        backgroundColor: colors,//提取颜色
                                        borderWidth: 1,//扇面之间的间隔空白
                                        data: datas//datas(每一个扇面的数值)
                                    }
                                  ]
                       };
    let chDonut = document.getElementById(chartid);//找到HTML中id为chartid的标签
    if (chDonut) {//如果找到HTML中id为chartid的标签
                  new Chart(chDonut, {//在这个chart的位置绘制新的图表
                      type: 'pie',//饼状图
                      data: chDonutData,//使用数据chDonutData
                      options: donutOptions//设置饼状图选项
                                     }
                            );
                  }
    }

//请求URL,获取JSON,并且通过JSON数据绘制各种图表
//URL:请求的URL
//chartid(HTML中canvas标签的名字)
//chart_type:图表类型
//labelname(图表的名称,例如CPU利用率)
function get_json_render_chart(url, chartid, chart_type, labelname="NoLabelName") {
            $.getJSON(url,function(data) {//请求URL的JSON,得到数据data,下面是对data的处理
                                            if (chart_type === "line")
                                            {
                                                chart_line(chartid, labelname, data.labels, data.datas, data.colors)
                                            }
                                            else if (chart_type === "bar")
                                            {
                                                chart_bar(chartid, labelname, data.labels, data.datas, data.colors)
                                            }
                                            else if (chart_type === "pie")
                                            {
                                                chart_pie(chartid, data.labels, data.datas, data.colors)
                                            }
                                          });
            }


//获取客户关于selected_chart_type(图表类型),selected_interval(刷新周期)和selected_deviceid(设备ID)的选择信息
//在chartid的canvas位置绘制图表
//labelname(图表的名称,例如CPU利用率)
function start_interval_updata_chart(selected_chart_type, selected_interval, selected_deviceid, chartid, labelname) {
     //获取客户关于selected_chart_type(图表类型)的选择信息
     let e = document.getElementById(selected_chart_type);
     let type = e.options[e.selectedIndex].value;
     //获取客户关于selected_interval(刷新周期)的选择信息
     let i = document.getElementById(selected_interval);
     let interval = i.options[i.selectedIndex].value;
     //拼接URL
     let url = "/chartjson/"+  type + "/" + selected_deviceid + "/"
     //绘制图表,并且设置刷新周期
     if (interval !== "None")
     {
         setInterval(function(){get_json_render_chart(url, chartid, type, labelname);},interval);
     }
     else
     {
         get_json_render_chart(url, chartid, type, labelname);
     }

    }

//与上述函数start_interval_updata_chart类似,只是不设置刷新周期(刷新周期的BUG未解决,进程会累加刷新)
function start_chart(selected_chart_type, selected_interval, selected_deviceid, chartid, labelname) {
     let e = document.getElementById(selected_chart_type);
     let type = e.options[e.selectedIndex].value;


     let i = document.getElementById(selected_interval);
     let interval = i.options[i.selectedIndex].value;

     let url = "/chartjson/"+  type + "/" + selected_deviceid + "/"


     get_json_render_chart(url, chartid, type, labelname);

    }


//为函数get_json_render_chart设置刷新周期
function json_start_interval_updata_chart(url, chartid, type, labelname, interval) {
     setInterval(function(){get_json_render_chart(url, chartid, type, labelname);},interval);
    }

//点击HTML中的按钮会出现下面的函数
//修改iframe url地址src的函数,提取MySelectMenu1中的选择,修改iframe1内的src值
function newSrc1() {
      var e = document.getElementById("MySelectMenu1");//读取MySelectMenu2内的选择
      var startchart1 = e.options[e.selectedIndex].value;//读取MySelectMenu2内的选择的值
      document.getElementById("iframe1").src=startchart1;//修改iframe2内的src链接
     }

//点击HTML中的按钮会出现下面的函数
//修改iframe url地址src的函数,提取MySelectMenu2中的选择,修改iframe2内的src值
function newSrc2() {
      var e = document.getElementById("MySelectMenu2");//读取MySelectMenu2内的选择
      var startchart2 = e.options[e.selectedIndex].value;//读取MySelectMenu2内的选择的值
      document.getElementById("iframe2").src=startchart2;//修改iframe2内的src链接
     }

//点击HTML中的按钮会出现下面的函数
//使用函数start_interval_updata_chart,绘制图表并且设置刷新周期
function json_chart1() {
        // start_chart("charttype1", "interval1", "1", "chart1", "CPU利用率");
        start_interval_updata_chart("charttype1", "interval1", "1", "chart1", "CPU利用率");
        }

//点击HTML中的按钮会出现下面的函数
//使用函数start_chart,绘制图表
function json_chart2() {
        // start_chart("charttype2", "interval2", "2", "chart2", "MEM利用率");
        start_interval_updata_chart("charttype2", "interval2", "2", "chart2", "MEM利用率");
        }