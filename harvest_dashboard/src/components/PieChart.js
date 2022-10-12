import React from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import moment from 'moment';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);


class PieChart extends React.Component {
  state = {
    labels: [],
    datasets: [],
    backgroundColors: [],
    total: 0,
  }

  fetchData() {
    const startTimeStr = this.props.startTime.utc().format();
    const endTimeStr = this.props.endTime.utc().format();
    const url = `${process.env.REACT_APP_BASE_API_URL}/api/v1/harvests/dashboard/?start_time=${startTimeStr}&end_time=${endTimeStr}&orchard_ids=${this.props.orchardIds}&group_by=${this.props.groupBy}&metric=${this.props.metric}`
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

  componentDidMount() {
    this.fetchData();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.startTime !== this.props.startTime ||
      prevProps.endTime !== this.props.endTime ||
      prevProps.orchardIds !== this.props.orchardIds ||
      prevProps.groupBy !== this.props.groupBy
    ) {
      this.fetchData();
    }
  }

  getTotalDisplay = () => {
    let total = ''
    let metric = ''
    if (this.props.metric === 'bin') {
      total = this.state.total.toLocaleString()
      metric = 'bins'
    }
    else {
      total = '$' + this.state.total.toLocaleString()
      metric = ''
    }
    return `${total} ${metric}`
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
      let tooltipEl = chart.canvas.parentNode.querySelector('#tooltipEl');

      if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.setAttribute('id', 'tooltipEl');
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
      const { chart, tooltip } = context;
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
          let text = document.createTextNode(
            moment(this.props.startTime).format('DD/MM/YYYY') + ' - ' + moment(this.props.endTime).format('DD/MM/YYYY')
          );
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
          value_div.style.marginLeft = '20px';
          value_div.style.background = '#fff';
          value_div.style.height = '20px';
          value_div.style.marginTop = '20px';
          value_div.style.marginBottom = '5px';
          value_div.style.display = 'inline-block';
          let span = document.createElement('span');
          text = document.createTextNode("");
          span.appendChild(text);
          span.style.color = '#DF1D00';

          let total = ''
          let metric = ''
          if (this.props.metric === 'bin') {
            total = context.tooltip.dataPoints[0].formattedValue + '&nbsp';
            metric = 'bins';
          }
          else {
            total = '$' + context.tooltip.dataPoints[0].formattedValue + '&nbsp';
            metric = '';
          }
          span.innerHTML = total;
          value_div.appendChild(span);
          span = document.createElement('span');
          text = document.createTextNode(metric);
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

        if (tableRoot) {
          // Remove old children
          while (tableRoot.firstChild) {
            tableRoot.firstChild.remove();
          }

          // Add new children
          tableRoot.appendChild(tableHead);
          tableRoot.appendChild(tableBody);
        }
      }

      const { offsetLeft: positionX, offsetTop: positionY } = chart.canvas;

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
      },
    }

    if (this.state.datasets.length === 0) {
      return (
        <div>No data available</div>
      )
    } else {
      return (
        <div className="pie">
          <Pie data={data} options={options} />
          <div className="chartName">{this.props.chartName}</div>
          <div className="total">TOTAL: {this.getTotalDisplay()}</div>
        </div>
      )
    }
  }
}

export default PieChart;
