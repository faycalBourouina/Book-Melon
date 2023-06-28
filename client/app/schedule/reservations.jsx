'use client';


import React, { useState, useEffect, useContext } from 'react';
import { useReservationsContext } from '../../context/ReservationsContext';

export default function Reservations() {
  const [message, setMessage] = useState('');
  const { myReservations, setMyReservations } = useReservationsContext();

  useEffect(() => {
    const fetchReservations = async () => {
      const response = await fetch('/api/reservations');
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        setMyReservations(data.reservations);
      } else {
        setMessage(data.message);
      }
    };
    fetchReservations();
  }, []);

  return (
    <div>
      <h1>My Reservations: </h1>
      {message && <p>{message}</p>}
      <ul>
        {myReservations.length > 0 && myReservations.map((reservation) => (
            <li key={reservation.id}>
              {reservation.date} {reservation.start_time} - {reservation.end_time}
            </li>
        ))}
      </ul>
    </div>
  );
}
