import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import axios from "axios";

interface UserTrack {
    id: string
    track: Track
    status: string
}

interface Track {
    spotify_id: string
    album: string
    artist: string
    duration_ms: number
    isrc: string
    title: string
    popularity: number
    spotify_image_link: string
}

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

function UserDetail() {
  const [userTracks, setUserTracks] = useState<UserTrack[]>([]);

  const { userId } = useParams();

  useEffect(() => {
    const fetchUsers = async () => {
      const result = await axios.get(
        `${import.meta.env.VITE_BACKEND_BASE_URL}/api/v1/users/${userId}/userTracks`
      );
      console.log(result);
      if (!result?.data?.length) {
        const result = await axios.post(
          `${import.meta.env.VITE_BACKEND_BASE_URL}/api/v1/users/${userId}/refreshUserTracks`
        );
        setUserTracks(result.data);
      }
      setUserTracks(result.data);
    };
    fetchUsers();
  }, [userId]);

  return (
    <div className="UserDetail">
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 700 }} aria-label="customized table">
          <TableHead>
            <TableRow>
              <StyledTableCell>Title</StyledTableCell>
              <StyledTableCell align="right">Artist</StyledTableCell>
              <StyledTableCell align="right">Popularity</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {userTracks.map((userTrack) => (
              <StyledTableRow key={userTrack.id}>
                <StyledTableCell component="th" scope="row">
                  {userTrack.track.title}
                </StyledTableCell>
                <StyledTableCell align="right">
                  {userTrack.track.artist}
                </StyledTableCell>
                <StyledTableCell align="right">
                  {userTrack.track.popularity}
                </StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default UserDetail;
