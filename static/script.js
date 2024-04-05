// Array to store book data
const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
    // Collect the book title and publication year
    const title = document.getElementById('bookTitle').value;
    const year = document.getElementById('publicationYear').value;
    const authors = Array.from(document.getElementsByClassName('authorName')).map(input => input.value).filter(Boolean);

    const data = {
        title: title,
        year: year,
        authors: authors
    };

    fetch('/api/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        document.getElementById('bookTitle').value = '';
        document.getElementById('publicationYear').value = '';
        const authorInputs = document.getElementsByClassName('authorName');
        while(authorInputs.length > 1) { // Keep one input field, remove the rest
            authorInputs[1].parentNode.removeChild(authorInputs[1]);
        }
        authorInputs[0].value = ''; // Clear the remaining input field
        showAllBooks();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function addAuthorInput() {
    const newInput = document.createElement("input");
    newInput.setAttribute("type", "text");
    newInput.setAttribute("class", "authorName");
    newInput.setAttribute("placeholder", "Author Name");
    document.getElementById("authorInputs").appendChild(newInput);
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear existing book list

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.innerHTML = `
            <h2>${book.title}</h2>
            <p>Publication Year: ${book.publication_year}</p>
            <p>Authors:</p>
            <ul>
                ${book.authors.map(author => `<li>${author}</li>`).join('')}
            </ul>
        `;
        bookList.appendChild(bookElement);
    });
}

// Function to fetch and display all books from the server
function showAllBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            const bookListElement = document.getElementById('bookList'); // Ensure this matches the ID in your HTML
            bookListElement.innerHTML = ''; // Clear existing book list

            data.books.forEach(book => {
                const authors = book.authors || 'No Authors Listed'; // Handle case when authors array is null or empty
                // Create the book element
                const bookElement = document.createElement('div');
                bookElement.innerHTML = `
                    <h2>${book.title}</h2>
                    <p>Publication Year: ${book.publication_year}</p>
                    <p>Authors: ${authors}</p>
                `;
                bookListElement.appendChild(bookElement);
            });
        })
        .catch(error => console.error('Error fetching all books:', error));
}


// Function to search books by year
function searchByYear() {
    const year = document.getElementById('searchYear').value; // Get the year from input

    fetch(`/api/search_books?year=${year}`) // Use template literals to include the year in the query
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.books && data.books.length > 0) {
                displaySearchResults(data.books); // Pass the 'books' array to the display function
            } else {
                displaySearchResults([]); // Pass an empty array to display no books found
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



// Function to display search results
function displaySearchResults(data) {
    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = '';

    if (data && data.length > 0) {
        data.forEach(book => {
            // Display each book
            const bookElement = document.createElement('div');
            bookElement.innerHTML = `
                <h2>${book.title}</h2>
                <p>Publication Year: ${book.publication_year}</p>
                <p>Authors: ${book.authors || 'No Authors Listed'}</p>
            `;
            searchResults.appendChild(bookElement);
        });
    } else {
        // Display a message indicating no books found
        searchResults.innerHTML = '<p>No books found for the specified year.</p>';
    }
}
