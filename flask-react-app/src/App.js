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
      <button className="sidebar-button" onClick={() => setActiveMenu('createRoles')}>
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

function CreateScenario({ roles }) {
  const [userStory, setUserStory] = useState('Корпоративная система');
  const [result, setData] = useState([])

  useEffect(() => {
    const fetchData = async () => {
        const response = await fetch('http://localhost:3000/api/create/create');
        const result = await response.json();
        setData(result);
  };
    fetchData();
  }, []);

  const [systems, setSystems] = useState([
    {
      name: 'Авторизация',
      enabled: true,
      components: [
        { name: 'Вход в систему', role: 'Пользователь', enabled: true },
        { name: 'Навигация', role: 'Пользователь', enabled: true },
        { name: 'Выход из системы', role: 'Пользователь', enabled: true },
        { name: 'Выход из учетной записи', role: 'Пользователь', enabled: true },
      ],
    },
  ]);

  const toggleSystem = (index) => {
    const newSystems = [...systems];
    newSystems[index].enabled = !newSystems[index].enabled;
    setSystems(newSystems);
  };

  const toggleComponent = (systemIndex, componentIndex) => {
    const newSystems = [...systems];
    newSystems[systemIndex].components[componentIndex].enabled = !newSystems[systemIndex].components[componentIndex].enabled;
    setSystems(newSystems);
  };

  const handleRoleChange = (systemIndex, componentIndex, role) => {
    const newSystems = [...systems];
    newSystems[systemIndex].components[componentIndex].role = role;
    setSystems(newSystems);
  };

  const handleCreateScenario = () => {
    console.log('Создать сценарий', { userStory, systems });
  };

  return (
    <div className="scenario-container">
      <h1>Введите название user story:</h1>
      <input
        type="text"
        value={userStory}
        onChange={(e) => setUserStory(e.target.value)}
        className="user-story-input"
      />
      <h2>Выберите составляющие системы</h2>
      {systems.map((system, systemIndex) => (
        <div key={systemIndex} className="system-container">
          <label className="switch">
            <input
              type="checkbox"
              checked={system.enabled}
              onChange={() => toggleSystem(systemIndex)}
            />
            <span className="slider round"></span>
          </label>
          <span>{system.name}</span>
          {system.enabled && system.components.map((component, componentIndex) => (
            <div key={componentIndex} className="component-container">
              <label className="switch">
                <input
                  type="checkbox"
                  checked={component.enabled}
                  onChange={() => toggleComponent(systemIndex, componentIndex)}
                />
                <span className="slider round"></span>
              </label>
              <span>{component.name}</span>
              <select
                value={component.role}
                onChange={(e) => handleRoleChange(systemIndex, componentIndex, e.target.value)}
                disabled={!component.enabled}
              >
                <option value="">Выбор роли</option>
                <option value="Пользователь">Пользователь</option>
                <option value="Администратор">Администратор</option>
              </select>
            </div>
          ))}
        </div>
      ))}
      <button onClick={handleCreateScenario} className="create-scenario-button">
        Создать сценарий
      </button>
    </div>
  );
}

function Roles({ roles, setRoles, setActiveMenu }) {

  const addRole = () => {
    setRoles([...roles, '']);
  };

  const removeRole = (index) => {
    setRoles(roles.filter((_, i) => i !== index));
  };

  const updateRole = (index, newRole) => {
    const newRoles = [...roles];
    newRoles[index] = newRole;
    setRoles(newRoles);
  };

 // const handleSkip = () => {
   // console.log('Пропустить');
  //};

   const handleApply = () => {
    console.log('Применить', roles);
    setActiveMenu('createScenario');
  };

  return (<div className="scenario-container">
      <h1>Задание ролей пользователей системы</h1>
      {roles.map((role, index) => (
        <div key={index} className="role-input-container">
          <input
            type="text"
            value={role}
            onChange={(e) => updateRole(index, e.target.value)}
            className="role-input"
          />
          <button onClick={() => removeRole(index)} className="remove-button">
            Удалить
          </button>
        </div>
      ))}
      <button onClick={addRole} className="add-role-button">
        Добавить роль
      </button>
      <div className="action-buttons">

        <button onClick={handleApply} className="apply-button">Применить</button>
      </div>
    </div>);
}
//<button onClick={handleSkip} className="skip-button">Пропустить</button>

function DashboardPage({ username, toggleSidebar, sidebarVisible, activeMenu, setActiveMenu }) {
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

  const [roles, setRoles] = useState([
            'Неавторизованный пользователь',
            'Пользователь',
            'Администратор',
  ]);

   const renderContent = () => {
    switch(activeMenu) {
      case 'viewProfiles':
        return <h2>Просмотр профилей</h2>;
      case 'createRoles':
        return (<Roles roles={roles} setRoles={setRoles} setActiveMenu={setActiveMenu}/>);
      case 'myScenarios':
        return <h2>Мои сценарии</h2>;
      case 'editScenarios':
        return <h2>Редактирование пользовательских сценариев</h2>;
      case 'createScenario':
        return <CreateScenario roles={roles}/>;
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
          <DashboardPage username={username} toggleSidebar={toggleSidebar}
          sidebarVisible={sidebarVisible} activeMenu={activeMenu} setActiveMenu={setActiveMenu}/>
        </>
      }
      <Sidebar isVisible={sidebarVisible} toggleSidebar={toggleSidebar} admin={admin} setActiveMenu={setActiveMenu}/> {/* Передаем setActiveMenu в Sidebar */}
    </div>
  );
}

export default App;