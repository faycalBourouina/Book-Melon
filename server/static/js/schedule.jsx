

const { useState } = React;

const Calendar = () => {
  const [selectedDate, setSelectedDate] = useState(null);

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  return (
    <div>
      <input type="date" onChange={handleDateChange} />
      {selectedDate && <p>Selected date: {selectedDate}</p>}
    </div>
  );
};