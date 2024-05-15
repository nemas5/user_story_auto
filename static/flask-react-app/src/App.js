import React, { useState } from 'react';
import './App.css'; // Подключаем файл стилей

function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    onLogin(username);
  };

  return (
    <div className="login-container">
      <h1>Авторизация</h1>
      <input
        type="text"
        placeholder="Имя пользователя"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="rounded-input" // Добавляем класс для скругления поля ввода
      />
      <input
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="rounded-input" // Добавляем класс для скругления поля ввода
      />
      <button onClick={handleLogin} className="rounded-button">Войти</button> {/* Добавляем класс для скругления кнопки */}
    </div>
  );
}

function Sidebar({ isVisible, toggleSidebar }) {
  const style = {
    width: isVisible ? '300px' : '0', // Устанавливаем ширину панели в зависимости от isVisible
    background: '#f0f0f0',
    padding: '20px',
    position: 'fixed',
    top: '0',
    left: isVisible ? '0' : '-300px', // Изменяем left в зависимости от isVisible
    bottom: '0',
    transition: 'left 0.3s ease, width 0.3s ease', // Анимация при изменении left и width
  };

  const buttonStyle = {
    position: 'absolute',
    top: '10px',
    left: '10px',
    zIndex: '9999',
    backgroundColor: 'transparent',
    color: '#007bff',
    border: 'none',
    cursor: 'pointer',
    fontSize: '20px',
  };

  return (
    <div style={style}>
      {isVisible && (
        <button onClick={toggleSidebar} style={buttonStyle}>
          &times;
        </button>
      )}
      <h2>Боковая панель</h2>
      <button className="sidebar-button">Кнопка 1</button>
      <button className="sidebar-button">Кнопка 2</button>
      <button className="sidebar-button">Кнопка 3</button>
      <button className="sidebar-button">Кнопка 4</button>
    </div>
  );
}

// Компонент рабочей страницы
function DashboardPage({ username, toggleSidebar }) {
  return (
    <div>
      <button className="sidebar-toggle-button" onClick={toggleSidebar}>Показать боковую панель</button>
      <h1>Привет, {username}!</h1>
    </div>
  );
}

// Компонент-обертка для приложения
function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [sidebarVisible, setSidebarVisible] = useState(false);

  const handleLogin = (username) => {
    setUsername(username);
    setLoggedIn(true);
  };

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  return (
    <div>
      {!loggedIn ?
        <LoginPage onLogin={handleLogin} /> :
        <DashboardPage username={username} toggleSidebar={toggleSidebar} />
      }
      <Sidebar isVisible={sidebarVisible} toggleSidebar={toggleSidebar}/>
    </div>
  );
}

export default App;
