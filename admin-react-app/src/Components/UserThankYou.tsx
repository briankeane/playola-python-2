import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

function UserSignedIn() {
  return (
    <div style={{ backgroundColor: 'black', justifyContent: 'center'}}>
      <Typography align='center'>
        <Button
        style={{
          borderRadius: 35,
          backgroundColor: "#DC625C",
          padding: "18px 36px",
          fontSize: "35px"
      }}
          color='primary'
          size='large'
          type='submit'
          variant='contained'
          sx={{mt: 10}}
        >
          Thank You
        </Button>
  </Typography>
    </div>
  )
}

export default UserSignedIn
