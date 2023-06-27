"use client";

import React, { useState, useEffect } from 'react';

export default function Reservations() {
  const [reservations, setReservations] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchReservations = async () => {
      const response = await fetch('/api/reservations');
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        setReservations(data.reservations);
      } else {
        setMessage(data.message);
      }
    };
    fetchReservations();
  }, []);

  return (
    <div>
      <h1>Reservations</h1>
      {message && <p>{message}</p>}
      <ul>
        {reservations.length > 0 && reservations.map((reservation) => (
            <li key={reservation.id}>
              {reservation.date} {reservation.start_time} - {reservation.end_time}
            </li>
        ))}
      </ul>
    </div>
  );
}
