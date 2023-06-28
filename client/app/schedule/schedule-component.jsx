import * as React from 'react';
import { useState, useEffect } from 'react';
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
  const [selectedTimeSlot, setSelectedTimeSlot] = useState('');
  const [timeSlots, setTimeSlots] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [message, setMessage] = useState('');
 
 
  // Function to fetch all reservations from the server
  const fetchReservations = async () => {
    const response = await fetch('/api/reservations/all');
    const data = await response.json();
    const { reservations } = data;
    setReservations(reservations);
  };


  // Function to check if a time slot is booked
  const isTimeSlotBooked = (date, timeSlot) => {
    const result = reservations.length > 0 &&
    reservations.some((reservation) => {
      return (
        reservation.date === date.format('YYYY-MM-DD') &&
        dayjs(reservation.start_time, 'HH:mm:ss').format('HH:mm') === dayjs(timeSlot, 'HH:mm').format('HH:mm')
      );
    });
    return result;
  };
  
  
  // Function to generate an array of available to time slots to book
  const generateTimeSlots = (date) => {
    const newTimeSlots = [];
    for (let i = 0; i < 24; i++) {
      const timeSlot1 = date.hour(i).minute(0);
      if (
        timeSlot1.isAfter(dayjs()) &&
        !isTimeSlotBooked(date, timeSlot1)
      ) {
        newTimeSlots.push(timeSlot1.format('h:mm A'));
      }
      const timeSlot2 = date.hour(i).minute(30);
      if (
        timeSlot2.isAfter(dayjs()) &&
        !isTimeSlotBooked(date, timeSlot2)
      ) {
        newTimeSlots.push(timeSlot2.format('h:mm A'));
      }
    }
    setTimeSlots(newTimeSlots);
  };
  
  // Fetch all reservations when the component is mounted 
  useEffect(() => {
    fetchReservations();
  }, []);

  // Call the generateTimeSlots when the selected date changes
  useEffect(() => {
    generateTimeSlots(value);
    console.log(reservations)
  }, [value, reservations]);

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
    const data = await response.json();
    if (response.ok) {
      setReservations(...reservations, data.reservation);
    } else {
      setMessage(data.message);
    }
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
      {/* Message component */}
      {message && <p>{message}</p>}
    </LocalizationProvider>
  );
}
