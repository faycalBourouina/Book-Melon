import { createContext } from 'react';
import { useContext } from 'react';

export const ReservationsContext = createContext();

export const useReservationsContext = () => useContext(ReservationsContext);