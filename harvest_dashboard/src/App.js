import React from 'react';
import Header from './components/Header';
import Filter from './components/Filter';
import Percentage from './components/Percentage';
import moment from 'moment';


class App extends React.Component {
  state = {
    startTime: moment('2021-01-01T00:00:00Z'),
    endTime: moment('2021-12-31T00:00:00Z'),
    orchardIds: '',
    groupBy: 'variety',
  }

  setStartTime = (time) => {
    this.setState({
      startTime: time
    })
  }

  setEndTime = (time) => {
    this.setState({
      endTime: time
    })
  }

  setOrchards = (ids) => {
    this.setState({
      orchardIds: ids
    })
  }

  setGroupBy = (value) => {
    this.setState({
      groupBy: value
    })
  }

  render () {
    const ColorMap = {
      '-M2StWPdhrsVWZjWluBD': '#77D5D4',
      '-M2StWPil_OVo67-CUm-': '#1A248A',
      '-M2StWPXh61bNCQDqglz' :'#F1E15A',
      '-M2StWPW7APCf0Jn3ew0': '#4ECB71',
      '-M2StWPSGN8EA4F04WlT': '#DF1D01',
    }
    return (
      <div className='App'>
        <Header />
        <Filter setStartTime={this.setStartTime} setEndTime={this.setEndTime} setOrchards={this.setOrchards} />
        <Percentage
          startTime={this.state.startTime} 
          endTime={this.state.endTime} 
          orchardIds={this.state.orchardIds} 
          colorMap={ColorMap}
          setGroupBy={this.setGroupBy}
          groupBy={this.state.groupBy}
        />
      </div>
    )
  }
}

export default App;