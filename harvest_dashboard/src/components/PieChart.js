import React from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);


class PieChart extends React.Component {
  state = {
    labels: [],
    datasets: [],
    backgroundColors: [],
    total: 0,
  }

  componentDidMount() {
    const url = `http://localhost:8000/api/v1/harvests/dashboard/?start_time=${this.props.startTime}&end_time=${this.props.endTime}&orchard_ids=${this.props.orchardIds}&group_by=${this.props.groupBy}&metric=${this.props.metric}`
    fetch(url, {
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then((result) => result.json())
      .then((result) => {
        this.setState({
          labels: result.map((item, index) => {
            return item.name
          }),
          datasets: result.map((item, index) => {
            return item.value
          }),
        })

        let total = 0;
        for (let i = 0; i < result.length; i++) {
          if (this.props.colorMap[result[i].gid] !== undefined) {
            this.state.backgroundColors.push(this.props.colorMap[result[i].gid])
            this.setState({
              backgroundColors: this.state.backgroundColors
            })
            total += result[i].value;
          }
        }
        this.setState({
          total: total
        })
      })
  }

  render() {
    const data = {
      labels: this.state.labels,
      datasets: [
        {
          data: this.state.datasets,
          backgroundColor: this.state.backgroundColors,
          borderWidth: 1,
        },
      ],
    };

    const getOrCreateTooltip = (chart) => {
      let tooltipEl = chart.canvas.parentNode.querySelector('div');
    
      if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.style.background = 'rgba(0, 0, 0, 0.7)';
        tooltipEl.style.borderRadius = '3px';
        tooltipEl.style.color = 'white';
        tooltipEl.style.opacity = 1;
        tooltipEl.style.pointerEvents = 'none';
        tooltipEl.style.position = 'absolute';
        tooltipEl.style.transform = 'translate(-50%, 0)';
        tooltipEl.style.transition = 'all .1s ease';
    
        const table = document.createElement('table');
        table.style.margin = '0px';
    
        tooltipEl.appendChild(table);
        chart.canvas.parentNode.appendChild(tooltipEl);
      }
    
      return tooltipEl;
    };
    
    const externalTooltipHandler = (context) => {
      // Tooltip Element
      const {chart, tooltip} = context;
      const tooltipEl = getOrCreateTooltip(chart);
    
      // Hide if no tooltip
      if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
      }
      // Set Text
      if (tooltip.body) {
        const titleLines = tooltip.title || [];
        const bodyLines = tooltip.body.map(b => b.lines);
        const tableHead = document.createElement('thead');
    
        titleLines.forEach(title => {
          const tr = document.createElement('tr');
          tr.style.borderWidth = 0;
    
          const th = document.createElement('th');
          th.style.borderWidth = 0;
          const text = document.createTextNode(title);
    
          th.appendChild(text);
          tr.appendChild(th);
          tableHead.appendChild(tr);
        });
    
        const tableBody = document.createElement('tbody');
        bodyLines.forEach((body, i) => {
          // add date time filter
          let text = document.createTextNode(this.props.startTime + ' - ' + this.props.endTime);
          let tr = document.createElement('tr');
          tr.style.backgroundColor = 'inherit';
          tr.style.borderWidth = 0;
          let td = document.createElement('td');
          td.appendChild(text);
          tr.appendChild(td);
          tableBody.appendChild(tr);
          
          // add data detail
          td = document.createElement('td');
          td.style.borderWidth = 0;
          
          let container = document.createElement("div");
          // container.style.display = 'flex';

          let name_div = document.createElement('div');
          name_div.style.background = '#fff';
          name_div.style.height = '20px';
          name_div.style.display = 'inline-block';
          name_div.style.marginTop = '20px';
          text = document.createTextNode(context.tooltip.dataPoints[0].label);
          name_div.style.color = '#DF1D00';
          name_div.appendChild(text);
          container.appendChild(name_div);

          let value_div = document.createElement('div');
          value_div.style.marginLeft = '50px';
          value_div.style.background = '#fff';
          value_div.style.height = '20px';
          value_div.style.marginTop = '20px';
          value_div.style.marginBottom = '5px';
          value_div.style.display = 'inline-block';
          let span = document.createElement('span');
          text = document.createTextNode(context.tooltip.dataPoints[0].formattedValue);
          span.appendChild(text);
          span.style.color = '#DF1D00';
          value_div.appendChild(span);
          span = document.createElement('span');
          text = document.createTextNode(this.props.metric + 's');
          span.appendChild(text);
          value_div.appendChild(span);
          container.appendChild(value_div);
          
          td.appendChild(container);
          tr = document.createElement('tr');
          tr.style.backgroundColor = 'inherit';
          tr.style.borderWidth = 0;
          tr.appendChild(td);
          tableBody.appendChild(tr);
        });
    
        const tableRoot = tooltipEl.querySelector('table');
    
        // Remove old children
        while (tableRoot.firstChild) {
          tableRoot.firstChild.remove();
        }
    
        // Add new children
        tableRoot.appendChild(tableHead);
        tableRoot.appendChild(tableBody);
      }
    
      const {offsetLeft: positionX, offsetTop: positionY} = chart.canvas;
    
      // Display, position, and set styles for font
      tooltipEl.style.opacity = 1;
      tooltipEl.style.left = positionX + tooltip.caretX + 'px';
      tooltipEl.style.top = positionY + tooltip.caretY + 'px';
      tooltipEl.style.font = tooltip.options.bodyFont.string;
      tooltipEl.style.padding = tooltip.options.padding + 'px ' + tooltip.options.padding + 'px';
      tooltipEl.style.backgroundColor = '#fff';
      tooltipEl.style.color = '#000';
    };
    
    const options = {
      plugins: {
        datalabels: {
          formatter: (value, ctx) => {
            const datapoints = ctx.chart.data.datasets[0].data
            const total = datapoints.reduce((total, datapoint) => total + datapoint, 0)
            const percentage = value / total * 100
            return percentage.toFixed(2) + '%';
          },
          color: '#fff',
        },
        tooltip: {
          enabled: false,
          position: 'nearest',
          external: externalTooltipHandler
        }
      }
    }
    return (
      <div>
        <Pie data={data} options={options} />
        <div>{this.props.chartName}</div>
        <div>TOTAL: {this.state.total} {this.props.metric}s</div>
      </div>
    )
  }
}

export default PieChart;
