module.exports = {
  testEnvironment: 'jsdom', // Use jsdom for DOM testing
  setupFilesAfterEnv: ['<rootDir>/jest.setup.cjs'], // Set up after env
  testMatch: ['**/*.test.js', '**/*.spec.js'], // Match test or spec files
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/__mocks__/fileMock.js',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
}
