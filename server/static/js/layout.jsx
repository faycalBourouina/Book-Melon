const Layout = ({ loggedUser }) => {
    return (
      <>
        {loggedUser && (
          <>
            <h3> Welcome {loggedUser} </h3>
            <div> My reservations</div>
          </>
        )}
        <h3> Please log in</h3>
        <div> search bar</div>
        <Calendar />
      </>
    );
  };