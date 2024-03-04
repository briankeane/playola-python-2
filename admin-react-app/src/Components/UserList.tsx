import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Button from "@mui/material/Button";
import axios from "axios";

interface User {
    id: string
    spotify_display_name: string
}

function UserList() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const result = await axios.get(`${import.meta.env.VITE_BACKEND_BASE_URL}/api/v1/users`);
    setUsers(result.data);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  function userItem(user: User) {
    return (
      <ListItem alignItems="flex-start">
        <Button
          component={Link}
          to={`/users/${user.id}`}
          variant="outlined"
          href="#outlined-buttons"
        >
          {user.spotify_display_name}
        </Button>
      </ListItem>
    );
  }
  const userListItems = users.map((user) => userItem(user));
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {userListItems}
    </List>
  );
}

export default UserList;
