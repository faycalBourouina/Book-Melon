import React, { useState } from 'react';
import { ReservationsContext } from './ReservationsContext';

export const ReservationsProvider = ({ children }) => {
  const [myReservations, setMyReservations] = useState([]);

  return (
    <ReservationsContext.Provider value={{ myReservations, setMyReservations }}>
      {children}
    </ReservationsContext.Provider>
  );
};