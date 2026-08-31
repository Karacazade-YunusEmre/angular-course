export interface Todo {
  readonly id: string;
  title: string;
  completed: boolean;
}

export type CreateTodoInput = Pick<Todo, 'title'>;

