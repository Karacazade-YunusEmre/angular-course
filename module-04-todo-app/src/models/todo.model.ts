export type Priority = 'low' | 'medium' | 'high';

export type FilterMode = 'all' | 'active' | 'completed';

export interface Todo {
  readonly id: string;
  title: string;
  completed: boolean;
  priority: Priority;
  readonly createdAt: Date;
}

export type CreateTodoInput = Omit<Todo, 'id' | 'createdAt'>;

export type UpdateTodoInput = Pick<Todo, 'title'>;
