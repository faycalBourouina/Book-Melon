import * as React from 'react';
import { useState } from 'react';
import dayjs from 'dayjs';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { StaticDatePicker } from '@mui/x-date-pickers/StaticDatePicker';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

export default function ScheduleComponent() {
  // State variables for the selected date and time slot
  const [value, setValue] = useState(dayjs());
  const [selectedTimeSlot, setSelectedTimeSlot] = useState(
    dayjs().format('h:mm A')
  );

  // Generate an array of time slots with a 30-minute interval
  const timeSlots = [];
  for (let i = 0; i < 24; i++) {
    const timeSlot1 = dayjs().hour(i).minute(0);
    if (timeSlot1.isAfter(dayjs())) {
      timeSlots.push(timeSlot1.format('h:mm A'));
    }
    const timeSlot2 = dayjs().hour(i).minute(30);
    if (timeSlot2.isAfter(dayjs())) {
      timeSlots.push(timeSlot2.format('h:mm A'));
    }
  }

  // Function to handle clicks on the "Book" button
  const handleBookClick = async () => {
    // Format the selected date and time slot as strings
    const date = value.format('MM/DD/YYYY');
    const startTime = dayjs(selectedTimeSlot, 'h:mm A').format('HH:mm');
    const endTime = dayjs(selectedTimeSlot, 'h:mm A')
      .add(30, 'minutes')
      .format('HH:mm');

    // Send a POST request to the server with the reservation data
    const response = await fetch('api/reservations/reservation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        date,
        start_time: startTime,
        end_time: endTime,
      }),
    });
    console.log("Booking: ", date, startTime, endTime);
    const data = await response.json();
    console.log(data);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      {/* Date picker component */}
      <StaticDatePicker
        displayStaticWrapperAs="desktop"
        value={value}
        onChange={(newValue) => {
          setValue(newValue);
        }}
        shouldDisableDate={(date) => date.isBefore(dayjs(), 'day')}
      />
      {/* Time slot selection component */}
      <Select
        value={selectedTimeSlot}
        onChange={(event) => setSelectedTimeSlot(event.target.value)}
      >
        {timeSlots.map((timeSlot) => (
          <MenuItem key={timeSlot} value={timeSlot}>
            {timeSlot}
          </MenuItem>
        ))}
      </Select>
      {/* Book button */}
      <Button onClick={handleBookClick}>Book</Button>
    </LocalizationProvider>
  );
}