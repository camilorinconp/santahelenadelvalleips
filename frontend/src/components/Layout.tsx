
import React from 'react';
import { Outlet, Link as RouterLink } from 'react-router-dom';
import { 
  AppBar, 
  Box, 
  Drawer, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText, 
  Toolbar, 
  Typography 
} from '@mui/material';
import { Home, People, FolderShared } from '@mui/icons-material'; // Icons

const drawerWidth = 240;

const navItems = [
  { text: 'Inicio', icon: <Home />, path: '/' },
  { text: 'Pacientes', icon: <People />, path: '/pacientes' },
  { text: 'Atenciones', icon: <FolderShared />, path: '/atenciones' },
];

export default function Layout() {
  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar 
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            IPS Santa Helena del Valle
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {navItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton component={RouterLink} to={item.path}>
                  <ListItemIcon>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {/* El Outlet renderizará la página actual que coincida con la ruta */}
        <Outlet />
      </Box>
    </Box>
  );
}
