import React from 'react'
import { DateRangePicker } from 'rsuite';
import { Dropdown } from 'semantic-ui-react'
import moment from 'moment';

const DateTimeFilter = (props) => {
  return (
    <div id="dateRangePicker">
      <fieldset>
        <legend>Date Range</legend>
        <DateRangePicker
          format="dd/MM/yyyy"
          placeholder="All time"
          defaultCalendarValue={[new Date("2021-05-01"), new Date("2021-12-31")]}
          character=' - '
          onChange={([startDate, endDate]) => {
            props.setStartTime(moment(startDate));
            props.setEndTime(moment(endDate));
          }}
        />
      </fieldset>
    </div>
  );
}

const OrchardsFilter = (props) => {
  const dropdownOptions = props.orchards.map((item, index) => {
    return {
      key: item.id,
      text: item.name,
      value: item.id,
    }
  });
  const handleOnChange = (e, data) => {
    props.setOrchards(data.value.join(','));
  }

  return (
    <div id="dropdown-orchards">
      <fieldset>
        <legend>Orchards</legend>
        <Dropdown
          placeholder='All'
          fluid
          multiple
          search
          selection
          options={dropdownOptions}
          onChange={handleOnChange}
        />
      </fieldset>
    </div>
  )
}

class Filter extends React.Component {
  state = {
    orchards: []
  }

  componentDidMount() {
    const url = `http://localhost:8000/api/v1/orchards/`
    fetch(url, {
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then((result) => result.json())
      .then((result) => {
        this.setState({
          orchards: result['results']
        })
      });
  }

  render() {
    return (
      <div id="filter">
        <DateTimeFilter setStartTime={this.props.setStartTime} setEndTime={this.props.setEndTime} />
        <OrchardsFilter orchards={this.state.orchards} setOrchards={this.props.setOrchards} />
      </div>
    )
  }
}

export default Filter;
