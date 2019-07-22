/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles(theme => ({
  root: {
    width: '100%',
		marginBottom: theme.spacing(2),
		overflowX: 'auto',
		maxHeight: '55vh',
  },
  table: {
  },
}));

export default function UserTable (props) {
	const classes = useStyles();
	const { users } = props;

	return (
		<Paper className={classes.root}>
			<Table className={classes.table}>
				<TableHead>
					<TableRow>
						<TableCell align="center">Name</TableCell>
						<TableCell align="center">LastName</TableCell>
						<TableCell align="center">Email</TableCell>
						<TableCell align="center">Age</TableCell>
						<TableCell align="center">Gender</TableCell>
						<TableCell align="center">Options</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{users.map(row => (
						<TableRow key={row._id}>
							<TableCell align="center">
								<a href="#" onClick={() => props.onClickCell('name', row.name, row)}>{row.name}</a>
							</TableCell>
							<TableCell align="center">
								<a href="#" onClick={() => props.onClickCell('last_name', row.last_name, row)} >{row.last_name}</a>
							</TableCell>
							<TableCell align="center">
								<a href="#" onClick={() => props.onClickCell('email', row.email, row)}>{row.email}</a>
							</TableCell>
							<TableCell align="center">
								<a href="#" onClick={() => props.onClickCell('age', row.age, row)}>{row.age}</a>
							</TableCell>
							<TableCell align="center">{row.gender}</TableCell>
							<TableCell align="center">
								<button
									className="btn btn-outline-info btn-sm"
									onClick={() => props.onDeleteUser(row._id)}
								>
									Delete
								</button>
							</TableCell>
						</TableRow>
					))}
				</TableBody>
			</Table>
		</Paper>
	);
}