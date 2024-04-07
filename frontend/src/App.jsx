import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route, Link } from 'react-router-dom';
import Chats from './components/Chats';
import Login from './components/Login';
import Registration from './components/Registration';
import Profile from './components/Profile'; 
// import './App.css'
import { AuthProvider, useAuth } from './context/auth';
import { UserProvider } from './context/user';
import AppNav from './components/AppNav';
import Button from './components/Button';

const queryClient = new QueryClient();

function Home() {
  // eslint-disable-next-line no-unused-vars
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="flex flex-col justify-center">
      <div className="text-center text-verdigris">
        Pony Express is an instant messaging application where users can talk to their friends.
      </div>
      <div className="flex justify-start">
        <Button>
          <Link to="/login">
            get started
          </Link>
        </Button>
      </div>
    </div>
  );
}

function Header(){
  return (
    <header>
      <AppNav />
    </header>
  )
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/chats" />} />
      <Route path="/chats" element={<Chats />}/>
      <Route path="/chats/:chatId" element={<Chats />}/>
      <Route path="/profile" element={<Profile />}/>
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnAuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Registration />} />
      <Route path="*" element={<Login />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();
  const className = isLoggedIn ? "flex grow justify-start" : "flex grow justify-center";

  return (
    <main className={className}>
      {isLoggedIn ? 
        <AuthenticatedRoutes /> :
        <UnAuthenticatedRoutes /> 
      }
    </main>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <UserProvider>
            <div className="flex flex-col h-screen max-h-screen">
              <Header />
              <Main />
            </div>
          </UserProvider> 
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

function NotFound() {
  return <h1>404: not found</h1>;
}

export default App
