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
    zIndex: '9999', // Поднимаем панель наверх
  };

  const buttonStyle = {
    position: 'absolute',
    top: '10px',
    right: '10px', // Перемещаем кнопку в правый верхний угол
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

function TopBar({ toggleSidebar }) {
  const topBarStyle = {
    background: '#007bff',
    color: '#fff',
    padding: '10px',
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100%',
    zIndex: '9998', // Уменьшаем z-index, чтобы не перекрывать боковую панель
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  return (
    <div style={topBarStyle}>
      <button className="toggle-sidebar-button" onClick={toggleSidebar}>
        &lt; Скрыть боковую панель
      </button>
      <div style={{ marginRight: '20px' }}>Пользователь</div>
    </div>
  );
}

function DashboardPage({ username, toggleSidebar, sidebarVisible }) {
  const dashboardStyle = {
    background: '#f0f0f0',
    padding: '20px',
    position: 'fixed',
    top: '50px', // Отступ сверху равен высоте верхней панели
    left: `${sidebarVisible ? '360px' : '20px'}`, // Отступ слева от боковой панели
    bottom: '20px',
    right: '20px', // Правый отступ равен 0, чтобы заполнить всю ширину
    transition: 'left 0.3s ease', // Анимация при изменении отступа слева
    borderRadius: '10px', // Скругление углов
    zIndex: '9997', // Уменьшаем z-index, чтобы не перекрывать боковую панель
  };

  return (
    <div style={dashboardStyle}>
      <TopBar toggleSidebar={toggleSidebar} />
      <h1>Привет!</h1>
    </div>
  );
}

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
        <DashboardPage username={username} toggleSidebar={toggleSidebar} sidebarVisible={sidebarVisible}/>
      }
      <Sidebar isVisible={sidebarVisible} toggleSidebar={toggleSidebar}/>
    </div>
  );
}

export default App;