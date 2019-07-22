const USERS_EP = 'http://127.0.0.1:5000/v1';
const NOTES_EP = 'http://127.0.0.1:5001/v1';

export const fetchUsers = (query, page, limit) => {
    let uri = `${USERS_EP}/users`;
    
    if (Object.keys(query).length) {
        uri += `?query=${JSON.stringify(query)}`;
    }

    if (page && limit) {
        const pref = Object.keys(query).length ? '&' : '?';
        uri += `${pref}page=${page}&limit=${limit}`;
    }

    return fetch(uri, {
        method: 'GET',
    });
}

export const fetchUserNotes = (userId) => {
    const uri = `${NOTES_EP}/user_notes?user_id=${userId}`;
    return fetch(uri, {
        method: 'GET',
    });
}

export const deleteUser = (userId) => {
    const uri = `${USERS_EP}/users/${userId}`;
    return fetch(uri, {
        method: 'DELETE',
    });
}

