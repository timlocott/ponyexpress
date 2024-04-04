import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import Chats from './components/Chats'
import './App.css'
import { AuthProvider, useAuth } from './context/auth';
import { UserProvider } from './context/user';

const queryClient = new QueryClient();

function Home() {
  // eslint-disable-next-line no-unused-vars
  const { isLoggedIn, logout } = useAuth();

  return (
    <div>
      <div>
        logged in: {isLoggedIn.toString()}
      </div>
    </div>
  );
}

function Header(){
  return (
    <header>
      Nav goes here
    </header>
  )
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chats" element={<Chats />}/>
      <Route path="/chats/:chatId" element={<Chats />}/>
      {/* <Route path="/profile" element={<Profile />}/> */}
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnAuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      {/* <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="*" element={<Login />} /> */}
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main>
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
            <div>
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
