import React from 'react'
import PieChart from './PieChart';
import { Tabs, TabLink }  from 'react-tabs-redux';


class Percentage extends React.Component {

  render() {
    return (
      <div id="percentage">
        <div className="percentage-container">
          <div className="header">
            <h2>PERCENTAGE</h2>
          </div>
          <div className="tabs">
          <Tabs
                name="tabs"
                onChange={(selectedTab, name) => {
                  this.props.setGroupBy(selectedTab);
                }}
                selectedTab="variety"
              >
                <TabLink to="variety">VARIETIES</TabLink>
                <TabLink to="orchard">ORCHARDS</TabLink>
              </Tabs>

          </div>
          <div className="charts">
            <div className="legend">
            </div>
            <div className="pie-container">
              <div className="piepie">
                <PieChart id="variety-bin"
                  startTime={this.props.startTime}
                  endTime={this.props.endTime}
                  orchardIds={this.props.orchardIds}
                  groupBy={this.props.groupBy}
                  metric="bin"
                  colorMap={this.props.colorMap}
                  chartName="Production"
                />
                <PieChart id="variety-cost"
                  startTime={this.props.startTime}
                  endTime={this.props.endTime}
                  orchardIds={this.props.orchardIds}
                  groupBy={this.props.groupBy}
                  metric="cost"
                  colorMap={this.props.colorMap}
                  chartName="Cost"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Percentage;
