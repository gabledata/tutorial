export interface Request {
  body: {
    id: string;
    numProducts: number;
    totalCost: number;
    userId: string;
    email: string;
  }
}

export interface Response {
  sendStatus: (status: number) => void;
}