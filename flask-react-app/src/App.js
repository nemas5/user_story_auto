import React, { useState, useEffect } from 'react';
import DocViewer, { DocViewerRenderers } from 'react-doc-viewer';
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

function DocumentViewer({ documents }) {
  console.log(documents);
  const handleExport = async (id) => {
    console.log(id);
    try {
      const response = await fetch(`http://localhost:3000/api/download/download/${id}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${id}.docx`; // Укажите имя файла для загрузки
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else {
        console.error('Failed to export file');
      }
    } catch (error) {
      console.error('Error exporting file:', error);
    }
  };

  return (
      <div className="my-scenarios-container">
        <div className="scenario-item">
          <span className="scenario-name">Сценарий успешно создан</span>
          <div className="scenario-buttons">
            <button className="export" onClick={() => handleExport(documents)}>Экспорт</button>
          </div>
        </div>
    </div>
  );
}

function CreateScenario({ roles, setActiveMenu, setDocuments }) {
  const [userStory, setUserStory] = useState('Корпоративная система');
  const [systems, setSystems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/create/create');
        const result = await response.json();
        if (Array.isArray(result)) {
          setSystems(result);
        } else {
          console.error('Received data is not an array:', result);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

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

  const toggleSubcomponent = (systemIndex, componentIndex, subcomponentIndex) => {
    const newSystems = [...systems];
    newSystems[systemIndex].components[componentIndex].components[subcomponentIndex].enabled = !newSystems[systemIndex].components[componentIndex].components[subcomponentIndex].enabled;
    setSystems(newSystems);
  };

  const handleRoleChange = (systemIndex, componentIndex, role) => {
    const newSystems = [...systems];
    newSystems[systemIndex].components[componentIndex].role = role;
    setSystems(newSystems);
  };

  const handleCreateScenario = async () => {
    let res = await fetch("http://localhost:3000/api/create/create", {
      method: "POST",
      headers: {
        'Content-Type':'application/json'
      },
      body: JSON.stringify({systems: systems, name: userStory, roles: roles}),
    });

    if (res.ok) {
      const data = await res.json();
      setDocuments(data);
      setActiveMenu('viewDocuments');
    } else {
      console.error('Failed to create scenario');
    }
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
                <option value='Любой пользователь'>Выбор роли</option>
                {roles.map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
              {component.enabled && component.components.map((subcomponent, subcomponentIndex) => (
                <div key={subcomponentIndex} className="subcomponent-container">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={subcomponent.enabled}
                      onChange={() => toggleSubcomponent(systemIndex, componentIndex, subcomponentIndex)}
                    />
                    <span className="slider round"></span>
                  </label>
                  <span>{subcomponent.name}</span>
                </div>
              ))}
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


function EditScenario({ editedRoles, setActiveMenu, curScenario }) {
  const [userStory, setUserStory] = useState('');
  const [systems, setSystems] = useState([]);

  useEffect(() => {
    const fetchScenarioData = async () => {
      try {
        const response = await fetch(`http://localhost:3000/api/view/edit/${curScenario}`);
        const result = await response.json();
        if (result) {
          setSystems(result.data);
          setUserStory(result.name);
          console.log(editedRoles);
        } else {
          console.error('Received data is not as expected:', result);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchScenarioData();
  }, [curScenario]);

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

  const toggleSubcomponent = (systemIndex, componentIndex, subcomponentIndex) => {
    const newSystems = [...systems];
    newSystems[systemIndex].components[componentIndex].components[subcomponentIndex].enabled = !newSystems[systemIndex].components[componentIndex].components[subcomponentIndex].enabled;
    setSystems(newSystems);
  };

  const handleRoleChange = (systemIndex, componentIndex, newRole) => {
    const newSystems = [...systems];
    newSystems[systemIndex].components[componentIndex].role = newRole;
    setSystems(newSystems);
  };

  const handleUpdateScenario = async () => {
    let res = await fetch(`http://localhost:3000/api/view/edit/${curScenario}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ systems, name: userStory, roles: editedRoles, s_id: curScenario })
    });

    if (res.ok) {
      console.log('Scenario updated successfully');
      // добавить setDocument
      setActiveMenu('viewDocuments');
    } else {
      console.error('Failed to update scenario');
    }
  };

  const getRoleOptions = () => {
    const roleOptions = [];
    // Добавляем роли из updatedRoles
    for (const roleId in editedRoles.updatedRoles) {
      roleOptions.push(editedRoles.updatedRoles[roleId]);
    }
    // Добавляем новые роли из newRoles
    roleOptions.push(...editedRoles.newRoles);
    return roleOptions;
  };

  return (
    <div className="scenario-container">
      <h1>Редактирование сценария</h1>
      <input
        type="text"
        value={userStory}
        onChange={(e) => setUserStory(e.target.value)}
        className="user-story-input"
      />
      <h2>Выберите составляющие системы</h2>
      {systems.length > 0 && systems.map((system, systemIndex) => (
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
          {system.enabled && system.components && system.components.map((component, componentIndex) => (
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
                onChange={(e) => handleRoleChange(systemIndex, componentIndex, e.target.value)}
                disabled={!component.enabled}
              >
                <option value='Выбор роли'>Выбор роли</option>
                {getRoleOptions().map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
              {component.enabled && component.components && component.components.map((subcomponent, subcomponentIndex) => (
                <div key={subcomponentIndex} className="subcomponent-container">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={subcomponent.enabled}
                      onChange={() => toggleSubcomponent(systemIndex, componentIndex, subcomponentIndex)}
                    />
                    <span className="slider round"></span>
                  </label>
                  <span>{subcomponent.name}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      ))}
      <button onClick={handleUpdateScenario} className="create-scenario-button">
        Обновить сценарий
      </button>
    </div>
  );
}


function EditRoles({ rolesFromServer, setActiveMenu, setEditedRoles }) {
  const [newRoles, setNewRoles] = useState([]);
  const [roles, setRoles] = useState({});
  const [deletedRoles, setDeletedRoles] = useState([]); // добавленный массив для хранения удалённых ролей

  useEffect(() => {
    // Инициализация ролей, полученных с сервера
    setRoles(rolesFromServer);
  }, [rolesFromServer]);

  const addRole = () => {
    setNewRoles([...newRoles, '']);
  };

  const removeRole = (index, isExistingRole = false) => {
    if (isExistingRole) {
      const updatedRoles = { ...roles };
      delete updatedRoles[index];
      setRoles(updatedRoles);
      setDeletedRoles([...deletedRoles, index]); // добавляем id удалённой роли в массив deletedRoles
    } else {
      setNewRoles(newRoles.filter((_, i) => i !== index));
    }
  };

  const updateRole = (index, newRole, isExistingRole = false) => {
    if (isExistingRole) {
      const updatedRoles = { ...roles };
      updatedRoles[index] = newRole;
      setRoles(updatedRoles);
    } else {
      const updatedNewRoles = [...newRoles];
      updatedNewRoles[index] = newRole;
      setNewRoles(updatedNewRoles);
    }
  };

  const handleApply = () => {
    const dataToSend = {
      updatedRoles: roles,
      newRoles: newRoles,
      deletedRoles: deletedRoles // добавляем удалённые роли в данные для отправки
    };
    setEditedRoles(dataToSend);
    setActiveMenu('editScenario');
    console.log('Применить', dataToSend);
  };

  return (
    <div className="scenario-container">
      <h1>Задание ролей пользователей системы</h1>
      {Object.keys(roles).map((id) => (
        <div key={id} className="role-input-container">
          <input
            type="text"
            value={roles[id]}
            onChange={(e) => updateRole(id, e.target.value, true)}
            className="role-input"
          />
          <button onClick={() => removeRole(id, true)} className="remove-button">
            Удалить
          </button>
        </div>
      ))}
      {newRoles.map((role, index) => (
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
    </div>
  );
}


function MyScenarios({ setActiveMenu, setRoles, setCurScenario }) {
  const [scenarios, setScenarios] = useState([]);

  useEffect(() => {
    // Функция для получения списка сценариев с сервера
    const fetchScenarios = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/view/view');
        const data = await response.json();
        setScenarios(data);
      } catch (error) {
        console.error('Ошибка при получении сценариев:', error);
      }
    };

    fetchScenarios();
  }, []);

  const handleEdit = async (id) => {
    try {
      const response = await fetch(`http://localhost:3000/api/view/role/${id}`);
      const data = await response.json();
      setCurScenario(id);
      setRoles(data);
      setActiveMenu('editRoles');
      // Добавьте логику для обработки результата редактирования
    } catch (error) {
      console.error('Ошибка при редактировании сценария:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:3000/api/view/delete/${id}`, { method: 'DELETE' });
      const data = await response.json();
      console.log('Удаление сценария:', data);
      setScenarios(scenarios.filter(scenario => scenario.id !== id));
    } catch (error) {
      console.error('Ошибка при удалении сценария:', error);
    }
  };

  const handleExport = async (id) => {
    try {
      const response = await fetch(`http://localhost:3000/api/download/download/${id}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${id}.docx`; // Укажите имя файла для загрузки
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else {
        console.error('Failed to export file');
      }
    } catch (error) {
      console.error('Error exporting file:', error);
    }
  };

  return (
    <div className="my-scenarios-container">
      <h2 className="my-scenarios-header">Выберите сценарий для редактирования</h2>
      {scenarios.map((scenario) => (
        <div key={scenario.id} className="scenario-item">
          <span className="scenario-name">{scenario.name}</span>
          <div className="scenario-buttons">
            <button className="edit" onClick={() => handleEdit(scenario.id)}>Редактировать</button>
            <button className="delete" onClick={() => handleDelete(scenario.id)}>Удалить</button>
            <button className="export" onClick={() => handleExport(scenario.id)}>Экспорт</button>
          </div>
        </div>
      ))}
    </div>
  );
}


function UserProfiles({ setActiveMenu }) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/users');
        const result = await response.json();
        if (result) {
          setUsers(result);
        } else {
          console.error('Received data is not as expected:', result);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchUsers();
  }, []);

  const handleDeleteUser = async (userId) => {
    try {
      const response = await fetch(`http://localhost:3000/api/users/del/${userId}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        setUsers(users.filter(user => user.id !== userId));
        console.log('User deleted successfully');
      } else {
        console.error('Failed to delete user');
      }
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handlePromoteUser = async (userId) => {
    try {
      const response = await fetch(`http://localhost:3000/api/users/prom/${userId}`,
      {
        method: 'POST'
      });
      if (response.ok) {
        const updatedUser = await response.json();
        console.log(updatedUser);
        setUsers(users.map(user => user.id === userId ? updatedUser : user));
        console.log('User promoted successfully');
      } else {
        console.error('Failed to promote user');
      }
    } catch (error) {
      console.error('Error promoting user:', error);
    }
  };

  return (
    <div className="user-profiles-container">
      <h1>Просмотр пользовательских профилей</h1>
      {users.map(user => (
        <div key={user.id} className="user-profile">
          <span>{user.id}</span>
          <div className="user-actions">
            {user.role === 'admin' ? (
              <span>Администратор</span>
            ) : (
              <>
                <button onClick={() => handlePromoteUser(user.id)}>Назначить администратором</button>
                <button onClick={() => handleDeleteUser(user.id)}>Удалить</button>
              </>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}


function DashboardPage({ username, toggleSidebar, sidebarVisible, activeMenu, setActiveMenu }) {
    const dashboardStyle = {
    display: 'flex',
    background: '#f0f0f0',
    padding: '20px',
    position: 'fixed',
    top: '70px',
    left: `${sidebarVisible ? '360px' : '20px'}`,
    right: '20px',
    bottom: '20px',
    transition: 'left 0.3s ease',
    borderRadius: '10px',
    zIndex: '9997',
    overflowY: 'auto',
  };

  const helloStyle = {
    justifyContent: 'center', // Центрируем по горизонтали
    alignItems: 'center', // Центрируем по вертикали
    margin: 'auto'
  };

  const initialRoles = [
    'Неавторизованный пользователь',
    'Пользователь',
    'Администратор',
  ];

  const [roles, setRoles] = useState(initialRoles);

  useEffect(() => {
    if (activeMenu === 'createRoles') {
      setRoles([...initialRoles]);  // reset roles to initial roles
    }
  }, [activeMenu]);

  const [documents, setDocuments] = useState([]);

  const [curScenario, setCurScenario] = useState('');

  const [editedRoles, setEditedRoles] = useState({});

  const renderContent = () => {
    switch (activeMenu) {
      case 'viewProfiles':
        return <UserProfiles setActiveMenu={setActiveMenu} />;
      case 'createRoles':
        return (<Roles roles={roles} setRoles={setRoles} setActiveMenu={setActiveMenu} />);
      case 'myScenarios':
        return <MyScenarios setActiveMenu={setActiveMenu} setRoles={setRoles} setCurScenario={setCurScenario} />;
      case 'editScenario':
        return <EditScenario editedRoles={editedRoles} setActiveMenu={setActiveMenu} curScenario={curScenario} />;
      case 'editRoles':
        return <EditRoles rolesFromServer={roles} setActiveMenu={setActiveMenu} setEditedRoles={setEditedRoles}/>
      case 'createScenario':
        return <CreateScenario roles={roles} setActiveMenu={setActiveMenu} setDocuments={setDocuments} />;
      case 'viewDocuments':
        return <DocumentViewer documents={documents} />;
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
          <DashboardPage
            username={username}
            toggleSidebar={toggleSidebar}
            sidebarVisible={sidebarVisible}
            activeMenu={activeMenu}
            setActiveMenu={setActiveMenu}
          />
        </>
      }
      <Sidebar
        isVisible={sidebarVisible}
        toggleSidebar={toggleSidebar}
        admin={admin}
        setActiveMenu={setActiveMenu}
      />
    </div>
  );
}

export default App;