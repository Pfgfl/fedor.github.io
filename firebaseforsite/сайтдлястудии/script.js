document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'contactsButton') {
           fetch('contacts.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});


document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'adressButton') {
           fetch('place.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});


document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'connectionButton') {
           fetch('connection.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});


document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'teachersButton') {
           fetch('teachers.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});

document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'main_siteButton') {
           fetch('main_window.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});


/*ДЛЯ TEACHERS.BUTTON*/

document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'teacher_ksenia_Button') {
           fetch('teacher_ksenia.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});

/*ДЛЯ BACK.BUTTON ДЛЯ ВСЕХ УЧИТЕЛЕЙ*/

document.addEventListener('DOMContentLoaded', () => {
   document.body.addEventListener('click', (event) => {
       if (event.target.id === 'backButton') {
           fetch('teachers.html')
               .then(response => {
                   if (!response.ok) {
                       throw new Error('Сетевая ошибка: ' + response.statusText);
                   }
                   return response.text();
               })
               .then(data => {
                   document.body.innerHTML = data;

                   // Обработчик для новой кнопки можно добавить здесь
               })
               .catch(error => {
                   console.error('Произошла ошибка при загрузке:', error);
               });
       }
    });
});

