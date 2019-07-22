import React, { Component } from 'react';
import Pagination from "react-js-pagination";
import { fetchUsers, fetchUserNotes, deleteUser } from '../services/userService';
import UserTable from './userTable';
import UserNotes from './userNotes';

const usersPerPage = 5;

export default class Users extends Component {
	
	state = {
		total: 0,
		activePage: 1,
		users: [],
		query: {},
		
		notes: [],
	}

	componentDidMount = () => {
		const { query, activePage } = this.state;
		this.fetchUsers(query, activePage);
	}

	fetchUsers = (query, page) => {
		fetchUsers(query, page, usersPerPage)
			.then(req => req.json())
			.then((resp) => {
				if (resp.success) {
					const users = resp.users.map(x => ({
						name: x.name,
						last_name: x.last_name,
						email: x.email,
						age: x.age,
						gender: x.gender,
						_id: x._id.$oid
					}));
					this.setState(prevState => ({ ...prevState, users, total: resp.count }));
				}
			}).catch(err => {
				console.error(err);
			});
	}

	fetchUserNotes = (userId) => {
		fetchUserNotes(userId)
			.then(req => req.json())
			.then((resp) => {
				if (resp.success) {
					const notes = resp.notes.map(x => ({
						title: x.title,
						body: x.body,
					}));
					this.setState(prevState => ({ ...prevState, notes }));
				}
			}).catch(err => {
				console.error(err);
			});
	}

	clearQuery = () => {
		this.setState(prevState => ({ ...prevState, query: {} }));
		this.fetchUsers({}, 1);
	}

	handleClickCell = (key, value, user) => {
		const { query } = this.state;
		query[key] = value;
		this.setState(prevState => ({ ...prevState, activePage: 1, query }));
		this.fetchUsers(query, 1);
		if (key === 'name') {
			this.fetchUserNotes(user._id);
		}
	}

	handleDeleteUsers = (userId) => {
		deleteUser(userId)
			.then(req => req.json())
			.then((resp) => {
				const { query, activePage } = this.state;
				this.fetchUsers(query, activePage);
			});
	}

	handlePageChange(activePage) {
		this.setState(prevState => ({ ...prevState, activePage }));
		this.fetchUsers(this.state.query, activePage);
  }

	render = () => {
		const { activePage, total, users, notes } = this.state;
		return (
			<div className="row">
				<div className={`col-${notes.length ? '9' : '12'} user-container`}>
					<div className="table-section">
						<h2 className="title text-center mb-3">Users List</h2>
						<UserTable
							users={users}
							onClickCell={this.handleClickCell}
							onDeleteUser={this.handleDeleteUsers}
						/>
						<Pagination
							activePage={activePage}
							itemsCountPerPage={usersPerPage}
							totalItemsCount={total}
							pageRangeDisplayed={5}
							onChange={(activePage) => this.handlePageChange(activePage)}
							itemClass="page-item"
							activeClass="active"
							disabledClass="disabled"
							prevPageText="Prev"
							nextPageText="Next"
							linkClass="page-link"
						/>
					</div>
					<div className="query">
							<h2 className="mb-3">Query: </h2>
							{JSON.stringify(this.state.query)}
						<br />
						<button className="btn btn-danger mt-4" onClick={this.clearQuery}>Clear Query</button>
					</div>
				</div>
				{notes.length ? (
					<div className="col-3 notes-container">
						<h2 className="title">Notes</h2>
						<UserNotes notes={notes} />
					</div>
				) : null}
			</div>
		);
	}
}