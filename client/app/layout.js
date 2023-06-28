'use client';

import { ReservationsProvider } from '../context/ReservationsProvider';
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>        
        <ReservationsProvider> {children} </ReservationsProvider>
      </body>
    </html>
  )
}
