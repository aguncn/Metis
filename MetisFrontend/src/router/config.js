import TabsView from '@/layouts/tabs/TabsView'
import BlankView from '@/layouts/BlankView'
import PageView from '@/layouts/PageView'

// 路由配置
const options = {
  routes: [
    {
      path: '/login',
      name: '登录页',
      component: () => import('@/pages/login')
    },
    {
      path: '*',
      name: '404',
      component: () => import('@/pages/exception/404'),
    },
    {
      path: '/403',
      name: '403',
      component: () => import('@/pages/exception/403'),
    },
    {
      path: '/',
      name: '首页',
      component: TabsView,
      redirect: '/login',
      children: [
				{
				  path: 'anomaly',
				  name: '异常时序',
				  meta: {
				    icon: 'dashboard',
				  },
				  component: PageView,
				  children: [
				    {
				      path: 'all_list',
				      name: '所有异常',
							meta: {
								label: 'all'
							},
				      component: () => import('@/pages/anomaly/list'),
				    },
						{
						  path: 'label_list',
						  name: '打标异常',
							meta: {
								label: 'yes'
							},
						  component: () => import('@/pages/anomaly/list'),
						}
				  ]
				},
				{
				  path: 'sample',
				  name: '样本库',
				  meta: {
				    icon: 'file-ppt',
				  },
				  component: () => import('@/pages/sample/list')
				},
        {
          path: 'task',
          name: '模型训练',
          meta: {
            icon: 'dashboard',
          },
          component: PageView,
          children: [
            {
              path: 'list',
              name: '训练任务列表',
							meta: {
								refresh: 'true'
							},
              component: () => import('@/pages/task/list'),
            },
        		{
        		  path: 'create',
        		  name: '新建训练任务',
        		  component: () => import('@/pages/task/create'),
        		}
          ]
        },
        {
          path: 'metric',
          name: '指标管理',
          meta: {
            icon: 'form'
          },
          component: PageView,
          children: [
            {
              path: 'viewset',
              name: '指标集',
              component: () => import('@/pages/metric/viewset/list'),
            },
						{
						  path: 'attr',
						  name: '指标',
						  component: () => import('@/pages/metric/attr/list'),
						}
          ]
        },
        {
          path: 'exception',
          name: 'API',
          meta: {
            icon: 'warning',
          },
          component: BlankView,
          children: [
            {
              path: '404',
              name: 'Exp404',
              component: () => import('@/pages/exception/404')
            },
            {
              path: '403',
              name: 'Exp403',
              component: () => import('@/pages/exception/403')
            },
            {
              path: '500',
              name: 'Exp500',
              component: () => import('@/pages/exception/500')
            }
          ]
        },
        {
          name: '验权页面',
          path: 'auth/demo',
          meta: {
            icon: 'file-ppt',
            authority: {
              permission: 'form',
              role: 'manager'
            },
            component: () => import('@/pages/demo')
          }
        }
      ]
    }
  ]
}

export default options
