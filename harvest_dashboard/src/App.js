import React from 'react';
import PieChart from './components/PieChart';


class App extends React.Component {
  state = {
    startTime: '2020-01-01T00:00:00Z',
    endTime: '2022-01-01T00:00:00Z',
    orchardIds: '',
  }

  render () {
    const varietyIdColorMap = {
      '-M2StWPdhrsVWZjWluBD': '#77D5D4',
      '-M2StWPil_OVo67-CUm-': '#1A248A',
      '-M2StWPXh61bNCQDqglz' :'#F1E15A',
      '-M2StWPW7APCf0Jn3ew0': '#4ECB71',
      '-M2StWPSGN8EA4F04WlT': '#DF1D01',
    }
    const groupByVariety = 'variety'
    const metricBin = 'bin'
    const groupByOrchard = 'orchard'
    const metricCost = 'cost'
    return (
      <div className='App'>
        <PieChart id="variety-bin"
          startTime={this.state.startTime} 
          endTime={this.state.endTime} 
          orchardIds={this.state.orchardIds} 
          groupBy={groupByVariety}
          metric={metricBin}
          colorMap={varietyIdColorMap}
          chartName="Production"
        />
      </div>
    )
  }
}

export default App;