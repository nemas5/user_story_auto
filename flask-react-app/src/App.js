import React, { useState, useEffect } from 'react';
import './App.css'; // Подключаем файл стилей

function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
  let res = await fetch("http://localhost:3000/api/auto/auto", {
    method: "POST",
    headers: {
      'Content-Type':'application/json'
    },
    body: JSON.stringify({
      login: username,
      password: password
    }),
  });
  //let data = await res.json();
  if (res.status == 200) {
    let data = await res.json();
    //setError(data.ad);
    onLogin(username, data.ad);
  }
  else {
    setError('Неверное имя пользователя или пароль!');
  }
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
      {error && <p>{error}</p>}
    </div>
  );
}

function Sidebar({ isVisible, toggleSidebar, admin, setActiveMenu }) {
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
      {admin && <button className="sidebar-button" onClick={() => setActiveMenu('viewProfiles')}>
        Просмотр профилей
      </button>}
      <button className="sidebar-button" onClick={() => setActiveMenu('createScenarios')}>
        Создание пользовательских сценариев
      </button>
      <button className="sidebar-button" onClick={() => setActiveMenu('myScenarios')}>
        Мои сценарии
      </button>
      {admin && <button className="sidebar-button"onClick={() => setActiveMenu('editScenarios')}>
        Редактирование пользовательских сценариев
      </button>}
    </div>
  );
}

function TopBar({ toggleSidebar, username }) {
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
        Показать боковую панель
      </button>
      <div style={{ marginRight: '20px' }}>{username}</div>
    </div>
  );
}

function DashboardPage({ username, toggleSidebar, sidebarVisible, activeMenu }) {
  const dashboardStyle = {
  display: 'flex', // Используем Flexbox
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

  const helloStyle = {
    justifyContent: 'center', // Центрируем по горизонтали
    alignItems: 'center', // Центрируем по вертикали
    margin: 'auto'
  };

   const renderContent = () => {
    switch(activeMenu) {
      case 'viewProfiles':
        return <h2>Просмотр профилей</h2>;
      case 'createScenarios':
        return <h2>Создание пользовательских сценариев</h2>;
      case 'myScenarios':
        return <h2>Мои сценарии</h2>;
      case 'editScenarios':
        return <h2>Редактирование пользовательских сценариев</h2>;
      default:
        return <h2 style={helloStyle}>Выберите раздел, чтобы приступить к работе</h2>;
    }
  };

  return (
    <div style={dashboardStyle}>
        {renderContent()}
    </div>
  );
}

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [admin, setAdmin] = useState(false);
  const [activeMenu, setActiveMenu] = useState('home');

  const handleLogin = (username, isAdmin) => {
    setUsername(username);
    setLoggedIn(true);
    if (isAdmin) {
      setAdmin(true);
    }
  };

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  return (
    <div>
      {!loggedIn ?
        <LoginPage onLogin={handleLogin} /> :
        <>
          <TopBar toggleSidebar={toggleSidebar} username={username} />
          <DashboardPage username={username} toggleSidebar={toggleSidebar} sidebarVisible={sidebarVisible} activeMenu={activeMenu}/>
        </>
      }
      <Sidebar isVisible={sidebarVisible} toggleSidebar={toggleSidebar} admin={admin} setActiveMenu={setActiveMenu}/> {/* Передаем setActiveMenu в Sidebar */}
    </div>
  );
}

export default App;