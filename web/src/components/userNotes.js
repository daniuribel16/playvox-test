import React from 'react';

export default function UserNotes (props) {
	const { notes } = props;

	return notes.map(x => (
		<div className="note shadow-sm">
			<h4>{x.title}</h4>
			<p>{x.body}</p>
		</div>
	));
}