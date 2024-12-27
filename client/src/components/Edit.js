// EditPage.js
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { TextField, Button, Typography, Paper } from "@mui/material";
import axios from "axios";

const EditPage = () => {
  const { userId } = useParams();
  const [user, setUser] = useState({
    name: "",
    email: "",
    phone_no: "",
  });
  const navigate = useNavigate();

  useEffect(() => {
    fetchUserDetails();
  }, []);

  const fetchUserDetails = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/users`);
      const foundUser = response.data.find((u) => u.id === parseInt(userId));
      if (foundUser) {
        setUser(foundUser);
      } else {
        alert("User not found!");
        navigate("/");
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUser({ ...user, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      await axios.patch(`http://127.0.0.1:5000/users/${userId}`, user);
      navigate("/");
    } catch (error) {
      console.error("Error updating user:", error);
    }
  };

  return (
    <Paper style={{ padding: "20px", maxWidth: "600px", margin: "20px auto" }}>
      <Typography variant="h5" gutterBottom>
        Edit User
      </Typography>
      <form>
        <TextField
          fullWidth
          margin="normal"
          label="Name"
          name="name"
          value={user.name}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          margin="normal"
          label="Email"
          name="email"
          value={user.email}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          margin="normal"
          label="Phone Number"
          name="phone_no"
          value={user.phone_no}
          onChange={handleInputChange}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          style={{ marginTop: "20px" }}
        >
          Save Changes
        </Button>
      </form>
    </Paper>
  );
};

export default EditPage;
