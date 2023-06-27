"use client";

import React, { useState, useEffect } from 'react';
import Reservation from './reservation';

export default function Reservations() {
  const [reservations, setReservations] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchReservations = async () => {
      const response = await fetch('/reservations');
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
                <Reservation reservation={reservation} />
            </li>
        ))}
      </ul>
    </div>
  );
}
