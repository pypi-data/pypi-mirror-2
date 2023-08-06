
google.load('visualization', '1', {'packages':['barchart']});
google.setOnLoadCallback(init);


function init() {
    var query = new google.visualization.Query('{{SITE_URL_PREFIX}}{% url chart_comp_json project.slug component.slug %}');
    query.send(handleResponse);
    drawToolbar();
}

function handleResponse(response) {
    if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
        return;
    }
    var data = response.getDataTable();

    container = document.getElementById('transifex_chart');
    container.style.textAlign = "center";
        
    chart_div = document.createElement('div');
    chart_div.style.width = "100%";
    chart_div.style.height = "210px";

    link_tx = document.createElement("a");
    link_tx.target = "_blank";
    link_tx.href = "{{SITE_URL_PREFIX}}{% url transifex.home %}";
    link_tx.title = "See more information on Transifex.net";
    link_tx.innerHTML = "<img border=\"0\" src=\"{{ STATIC_URL }}charts/images/tx-logo-micro.png\"/>";

    link_comp = document.createElement("a");
    link_comp.target = "_blank";
    link_comp.style.textDecoration = "none";
    link_comp.style.color = "black";
    link_comp.style.fontSize = "66%";
    link_comp.href = "{{SITE_URL_PREFIX}}{% url component_detail project.slug component.slug %}";
    link_comp.innerHTML = "Top translations: {{project.name}} » {{component.name}}";


    container.innerHTML = "";
    container.appendChild(link_comp);
    container.appendChild(chart_div);
    container.appendChild(link_tx);

    var chart = new google.visualization.BarChart(chart_div);
    chart.draw(data, {
        isStacked : true,
        min : 0,
//        title : "Project: {{project.name}} >> {{component.name}}",
        legend : "none",
        titleColor : '333333',
        colors : ['78dc7d', 'dae1ee', 'efefef'],
    });
}

