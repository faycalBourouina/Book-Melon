const {useState} = React;

const App = ({userName}) => {
    const [loggedUser, setLoggedUser] = useState(userName);

    return (
        <>
            <Layout loggedUser={loggedUser} />     
        </>

    )
}