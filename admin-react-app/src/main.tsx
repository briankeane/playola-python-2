import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ErrorPage from './Components/ErrorPage.tsx';
import Root from './Components/Root.tsx';
import UserDetail from './Components/UserDetail.tsx';
import './index.css';
import UserList from './Components/UserList.tsx';
import UserSignIn from './Components/UserSignIn.tsx';
import UserThankYou from './Components/UserThankYou.tsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
        {
          path: "userSignIn",
          element: <UserSignIn />
        },
        {
          path: "userThankYou",
          element: <UserThankYou />
        },
      {
        path: "users",
        element: <UserList />,
      },
      {
        path: "users/:userId",
        element: <UserDetail />,
      }
    ]
  }
]);


ReactDOM.createRoot(document.getElementById('root')!).render(
  <>
    <RouterProvider router={router} />
  </>,
)
