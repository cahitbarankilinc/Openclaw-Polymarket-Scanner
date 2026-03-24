# Session: 2026-03-07 21:49:06 UTC

- **Session Key**: agent:main:main
- **Session ID**: cfc96578-b107-4bd7-bc2f-48603c651dc4
- **Source**: webchat

## Conversation Summary

user: A new session was started via /new or /reset. Execute your Session Startup sequence now - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
assistant: [[reply_to_current]] Hey — I’m online and ready to roll. I’m practical, direct, and happy to dive into whatever you need. What do you want to tackle first?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-06 23:35 GMT+1] daha önce lokal llm modelleri test icin farkli seviyelerdetestler yapmistik. simdi senden istedigim, bana yeni test promtlari yaz, cevabi uzun bir kod olsun, bakalim llm modelleri ne kadar uzun cevaplar yazacaklar, testi hangisi daha iyi cevaplicak onu görücez. simdi bana direkt copy paste yapabilecegim promtu yaz, istedigin bir alanda olabilir
assistant: [[reply_to_current]] Süper fikir. Aşağıyı **direkt kopyala-yapıştır**:

```text
ROLÜN: Kıdemli yazılım mimarı ve principal engineer’sin.

GÖREV: Tek bir yanıtta, SADECE KOD üreterek (açıklama yok), production-grade, devasa bir proje iskeleti yaz.

HEDEF DİL/TEKNOLOJİ:
- TypeScript (Node.js 22)
- Fastify backend
- PostgreSQL (Prisma ORM)
- Redis cache + queue
- WebSocket realtime
- JWT + refresh token auth
- RBAC (admin/editor/viewer)
- Rate limit, audit log, healthcheck, metrics
- OpenAPI/Swagger
- Vitest testleri
- Docker + docker-compose
- GitHub Actions CI
- Seed script + migration + örnek veriler

ÇIKTI FORMATI (ZORUNLU):
1) Yalnızca kod blokları üret.
2) Her dosyayı şu başlıkla ver:
   // FILE: <path/to/file>
3) Sonra o dosyanın tam içeriğini ver.
4) En az 30 dosya üret.
5) Toplam çıktı en az 2500 satır kod olsun.
6) Kodlar birbiriyle tutarlı ve çalıştırılabilir olsun.
7) Türkçe veya İngilizce açıklama, yorum, özet YAZMA. Sadece kod.
8) “continue?” diye sorma; tek mesajda bitir.
9) Kısaltma, placeholder, TODO, pseudo-code YASAK. Gerçek implementasyon yaz.
10) Tüm import’lar geçerli olmalı, tipler eksiksiz olmalı.

İŞ KAPSAMI (MUTLAKA DAHİL):
- Monorepo yapısı:
  - apps/api
  - packages/shared
  - infra
- Auth:
  - register/login/refresh/logout/me
  - password hash (argon2)
  - access+refresh token rotasyonu
- Users:
  - CRUD + pagination + filtering + sorting
- Projects & Tasks domain:
  - Project CRUD
  - Task CRUD
  - Task status flow: todo -> in_progress -> blocked -> done
  - optimistic locking (version alanı)
- Realtime:
  - Task update event broadcast
- Observability:
  - pino logger
  - request-id middleware
  - /health, /ready, /metrics endpointleri
- Security:
  - helmet/cors/sanitize
  - rate limit by IP + by user
  - permission guard
- Test:
  - unit + integration + e2e (Vitest)
  - en az 20 test dosyası
- CI:
  - lint + typecheck + test + build pipeline
- Infra:
  - Dockerfile (multi-stage)
  - docker-compose (api+db+redis)
  - .env.example

KALİTE KRİTERLERİ:
- SOLID prensiplerine uygun katmanlı mimari
- Zod ile request/response validation
- Hata yönetimi için merkezi error handler
- Repository + Service + Controller ayrımı
- Prisma schema detaylı ve ilişkiler doğru
- Seed script gerçekçi demo data üretsin
- Kod stili tutarlı, strict TypeScript aktif

BAŞLA.
```

İstersen bir sonraki adımda sana bunun **Python/FastAPI** veya **Go/Fiber** versiyonunu da aynı “uzun çıktı testi” formatında vereyim.
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-06 23:45 GMT+1] Model 1(tam ismi vermicem degerlendirirken adil olsun) asagidaki output u cikartti, asagidaki kodu kontrol et ve farkli metriklerle puanla. toplamda 6 dakika 20 saniye sürdü:

// FILE: monorepo/tsconfig.json
```typescript
{
 "compilerOptions": {
 "target": "ES2022",
 "module": "commonjs",
 "strict": true,
 "esModuleInterop": true,
 "skipLibCheck": true,
 "forceConsistentCasingInFileNames": true,
 "moduleResolution": "node",
 "outDir": "dist",
 "rootDir": "src",
 "baseUrl": ".",
 "paths": {
 "@shared/*": ["packages/shared/src/*"],
 "@api/*": ["apps/api/src/*"],
 "@infra/*": ["infra/*"]
 },
 "lib": ["ES2022", "DOM"],
 "types": ["node"],
 "noEmit": false,
 "incremental": true,
 "resolveJsonModule": true,
 "isolatedModules": true,
 "noFallthroughCasesInSwitch": true,
 "noImplicitReturns": true,
 "noUnusedLocals": true,
 "noUnusedParameters": true,
 "noImplicitThis": true,
 "alwaysStrict": true,
 "experimentalDecorators": true,
 "emitDecoratorMetadata": true,
 "skipDefaultLibCheck": true,
 "declaration": true,
 "declarationDir": "dist/types"
 },
 "exclude": ["node_modules", "dist", "test", "scripts"]
}
```

// FILE: monorepo/apps/api/src/main.ts
```typescript
import { app } from '@api/server'
import { setupRedis } from '@infra/redis'
import { setupDatabase } from '@infra/database'
import { setupAuth } from '@api/auth'
import { setupRoutes } from '@api/routes'
import { setupWebSocket } from '@api/websocket'
import { setupObservability } from '@api/observability'
import { setupSecurity } from '@api/security'

async function bootstrap() {
 await setupDatabase()
 await setupRedis()

 setupAuth()
 setupRoutes(app)
 setupWebSocket(app)
 setupObservability(app)
 setupSecurity(app)

 const port = process.env.PORT || 3000
 app.listen({ port }, () => {
 console.log(`[main] Server running on port ${port}`)
 })
}

bootstrap().catch(console.error)
```

// FILE: monorepo/apps/api/src/server.ts
```typescript
import fastify from 'fastify'
import fastifyHelmet from '@fastify/helmet'
import fastifyCors from '@fastify/cors'
import fastifySanitize from '@fastify/sanitize'
import fastifyRateLimit from '@fastify/rate-limit'
import fastifySwagger from '@fastify/swagger'
import fastifySwaggerUi from '@fastify/swagger-ui'
import fastifyTypeBox from '@fastify/type-provider-typebox'
import { ZodError } from 'zod'
import { logger } from '@api/observability/logger'
import { errorHandler } from '@api/middleware/errorHandler'
import { requestIdMiddleware } from '@api/middleware/requestId'

export const app = fastify({
 logger,
 bodyLimit: 10 * 1024 * 1024, // 10MB
 ajv: {
 customErrors: true,
 removeEmpty: true,
 allErrors: true
 }
}).withTypeProvider<typeof import('@fastify/type-provider-typebox')>()

app.register(fastifyHelmet)
app.register(fastifyCors, {
 origin: process.env.CORS_ORIGIN || '*',
 methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
})
app.register(fastifySanitize)
app.register(fastifyRateLimit, {
 max: 100,
 ban: 101,
 timeWindow: 60 * 1000
})

app.register(fastifySwagger, {
 openapi: {
 info: {
 title: 'Task Management API',
 description: 'Production-grade task management system',
 version: '1.0.0'
 },
 servers: [{ url: '/', description: 'Development' }]
 }
})

app.register(fastifySwaggerUi, {
 routePrefix: '/docs',
 swaggerOptions: {
 url: '/swagger.json'
 }
})

app.register(fastifyTypeBox)

app.setErrorHandler(errorHandler)
app.addHook('preHandler', requestIdMiddleware)

declare module 'fastify' {
 interface FastifyRequest {
 requestId: string
 user?: {
 id: string
 role: 'admin' | 'editor' | 'viewer'
 }
 }
}
```

// FILE: monorepo/apps/api/src/auth/auth.ts
```typescript
import fastify from 'fastify'
import fastifyJwt from '@fastify/jwt'
import fastifyCookie from '@fastify/cookie'
import { argon2id } from 'argon2'
import { v4 as uuidv4 } from 'uuid'
import { User } from '@shared/domain/user'
import { UserRepository } from '@shared/repository/user'
import { AuthService } from '@shared/service/auth'
import { AuthController } from '@shared/controller/auth'

export async function setupAuth() {
 const app = fastify

 app.register(fastifyJwt, {
 secret: process.env.JWT_SECRET || 'default-secret',
 cookie: {
 cookieName: 'taskly_token',
 signed: true
 }
 })

 app.register(fastifyCookie)

 const userRepo = new UserRepository()
 const authService = new AuthService(userRepo)
 const authController = new AuthController(authService)

 app.post('/auth/register', authController.register)
 app.post('/auth/login', authController.login)
 app.post('/auth/refresh', authController.refresh)
 app.post('/auth/logout', authController.logout)
 app.get('/auth/me', authController.me)

 app.decorate('auth', {
 hashPassword: async (password: string) => {
 return argon2id.encode(password, {
 type: argon2id.argon2id,
 memoryCost: 19456,
 timeCost: 3,
 outputLen: 32,
 hashLength: 32
 })
 },
 verifyPassword: async (password: string, hash: string) => {
 return argon2id.verify(hash, password)
 }
 })
}
```

// FILE: monorepo/apps/api/src/auth/routes.ts
```typescript
import { FastifyInstance } from 'fastify'
import { AuthController } from '@shared/controller/auth'
import { AuthService } from '@shared/service/auth'
import { UserRepository } from '@shared/repository/user'

export function setupAuthRoutes(app: FastifyInstance) {
 const userRepo = new UserRepository()
 const authService = new AuthService(userRepo)
 const authController = new AuthController(authService)

 app.post('/auth/register', authController.register)
 app.post('/auth/login', authController.login)
 app.post('/auth/refresh', authController.refresh)
 app.post('/auth/logout', authController.logout)
 app.get('/auth/me', authController.me)
}
```

// FILE: monorepo/apps/api/src/controller/auth.ts
```typescript
import { FastifyReply, FastifyRequest } from 'fastify'
import { z } from 'zod'
import { AuthService } from '@shared/service/auth'
import { AuthError } from '@shared/error/auth'

const RegisterSchema = z.object({
 email: z.string().email(),
 password: z.string().min(8),
 name: z.string().min(2)
})

const LoginSchema = z.object({
 email: z.string().email(),
 password: z.string().min(8)
})

export class AuthController {
 constructor(private authService: AuthService) {}

 async register(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const body = RegisterSchema.parse(request.body)
 const user = await this.authService.register(body)
 return reply.status(201).send(user)
 }

 async login(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const body = LoginSchema.parse(request.body)
 const { accessToken, refreshToken } = await this.authService.login(body)
 return reply
 .setCookie('access_token', accessToken, {
 httpOnly: true,
 secure: process.env.NODE_ENV === 'production',
 sameSite: 'strict'
 })
 .setCookie('refresh_token', refreshToken, {
 httpOnly: true,
 secure: process.env.NODE_ENV === 'production',
 sameSite: 'strict'
 })
 .status(200)
 .send({ accessToken, refreshToken })
 }

 async refresh(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { refreshToken } = request.cookies
 if (!refreshToken) throw new AuthError('Refresh token required')

 const { accessToken, newRefreshToken } = await this.authService.refresh(refreshToken)
 return reply
 .setCookie('access_token', accessToken, {
 httpOnly: true,
 secure: process.env.NODE_ENV === 'production',
 sameSite: 'strict'
 })
 .setCookie('refresh_token', newRefreshToken, {
 httpOnly: true,
 secure: process.env.NODE_ENV === 'production',
 sameSite: 'strict'
 })
 .status(200)
 .send({ accessToken, newRefreshToken })
 }

 async logout(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { refreshToken } = request.cookies
 if (!refreshToken) return reply.status(200).send({})

 await this.authService.invalidateRefreshToken(refreshToken)
 return reply
 .clearCookie('access_token')
 .clearCookie('refresh_token')
 .status(200)
 .send({})
 }

 async me(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const user = request.user
 if (!user) throw new AuthError('Unauthorized')

 return reply.status(200).send({
 id: user.id,
 email: user.email,
 name: user.name,
 role: user.role
 })
 }
}
```

// FILE: monorepo/apps/api/src/controller/user.ts
```typescript
import { FastifyReply, FastifyRequest } from 'fastify'
import { z } from 'zod'
import { UserService } from '@shared/service/user'
import { UserError } from '@shared/error/user'
import { PermissionGuard } from '@shared/middleware/permission'

const CreateUserSchema = z.object({
 email: z.string().email(),
 password: z.string().min(8),
 name: z.string().min(2),
 role: z.enum(['admin', 'editor', 'viewer'])
})

const UpdateUserSchema = z.object({
 name: z.string().min(2).optional(),
 role: z.enum(['admin', 'editor', 'viewer']).optional()
})

export class UserController {
 constructor(private userService: UserService) {}

 async create(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const body = CreateUserSchema.parse(request.body)
 const user = await this.userService.create(body)
 return reply.status(201).send(user)
 }

 async getAll(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { page = 1, limit = 10 } = request.query
 const users = await this.userService.getAll({
 page: Number(page),
 limit: Number(limit)
 })
 return reply.status(200).send(users)
 }

 async getById(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { id } = request.params
 const user = await this.userService.getById(id)
 if (!user) throw new UserError('User not found')

 return reply.status(200).send(user)
 }

 async update(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { id } = request.params
 const body = UpdateUserSchema.parse(request.body)

 await PermissionGuard.check(request, 'update_user', id)
 const user = await this.userService.update(id, body)
 return reply.status(200).send(user)
 }

 async delete(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { id } = request.params
 await PermissionGuard.check(request, 'delete_user', id)
 await this.userService.delete(id)
 return reply.status(204).send()
 }
}
```

// FILE: monorepo/apps/api/src/controller/project.ts
```typescript
import { FastifyReply, FastifyRequest } from 'fastify'
import { z } from 'zod'
import { ProjectService } from '@shared/service/project'
import { ProjectError } from '@shared/error/project'
import { PermissionGuard } from '@shared/middleware/permission'

const CreateProjectSchema = z.object({
 name: z.string().min(2),
 description: z.string().optional(),
 ownerId: z.string()
})

const UpdateProjectSchema = z.object({
 name: z.string().min(2).optional(),
 description: z.string().optional()
})

export class ProjectController {
 constructor(private projectService: ProjectService) {}

 async create(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const body = CreateProjectSchema.parse(request.body)
 const project = await this.projectService.create(body)
 return reply.status(201).send(project)
 }

 async getAll(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { page = 1, limit = 10 } = request.query
 const projects = await this.projectService.getAll({
 page: Number(page),
 limit: Number(limit)
 })
 return reply.status(200).send(projects)
 }

 async getById(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { id } = request.params
 const project = await this.projectService.getById(id)
 if (!project) throw new ProjectError('Project not found')

 return reply.status(200).send(project)
 }

 async update(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { id } = request.params
 const body = UpdateProjectSchema.parse(request.body)

 await PermissionGuard.check(request, 'update_project', id)
 const project = await this.projectService.update(id, body)
 return reply.status(200).send(project)
 }

 async delete(
 request: FastifyRequest,
 reply: FastifyReply
 ) {
 const { id } = request.params
 await PermissionGuard.check(request, 'delete_project', id)
 await this.projectService.delete(id)
 return reply.status(204).send()
 }
}
```

// FILE: monorepo/apps/api/src/error/auth.ts
```typescript
export class AuthError extends Error {
 constructor(message: string) {
 super(message)
 this.name = 'AuthError'
 }
}

export class TokenError extends Error {
 constructor(message: string) {
 super(message)
 this.name = 'TokenError'
 }
}
```

// FILE: monorepo/apps/api/src/error/project.ts
```typescript
export class ProjectError extends Error {
 constructor(message: string) {
 super(message)
 this.name = 'ProjectError'
 }
}
```

// FILE: monorepo/apps/api/src/error/user.ts
```typescript
export class UserError extends Error {
 constructor(message: string) {
 super(message)
 this.name = 'UserError'
 }
}
```

// FILE: monorepo/apps/api/src/middleware/permission.ts
```typescript
import { FastifyRequest } from 'fastify'
import { AuthError } from '@shared/error/auth'

export class PermissionGuard {
 static async check(
 request: FastifyRequest,
 permission: string,
 resourceId?: string
 ) {
 const user = request.user
 if (!user) throw new AuthError('Unauthorized')

 const requiredPermission = `${permission}_${resourceId || ''}`

 // In a real application, you would check against a permission system
 // For this example, we'll use simple role-based checks
 if (user.role === 'admin') return

 if (user.role === 'editor') {
 if (requiredPermission.startsWith('update_') || requiredPermission.startsWith('delete_')) {
 throw new AuthError('Insufficient permissions')
 }
 }

 if (user.role === 'viewer') {
 throw new AuthError('Insufficient permissions')
 }
 }
}
```

// FILE: monorepo/apps/api/src/repository/user.ts
```typescript
import { PrismaClient } from '@prisma/client'
import { User } from '@shared/domain/user'

export class UserRepository {
 private prisma = new PrismaClient()

 async create(user: Omit<User, 'id'>): Promise<User> {
 return this.prisma.user.create({
 data: user
 })
 }

 async findByEmail(email: string): Promise<User | null> {
 return this.prisma.user.findUnique({
 where: { email }
 })
 }

 async findById(id: string): Promise<User | null> {
 return this.prisma.user.findUnique({
 where: { id }
 })
 }

 async findMany(options: {
 page: number
 limit: number
 }): Promise<User[]> {
 const skip = (options.page - 1) * options.limit
 return this.prisma.user.findMany({
 skip,
 take: options.limit
 })
 }

 async update(id: string, data: Partial<User>): Promise<User> {
 return this.prisma.user.update({
 where: { id },
 data
 })
 }

 async delete(id: string): Promise<User> {
 return this.prisma.user.delete({
 where: { id }
 })
 }
}
```

// FILE: monorepo/apps/api/src/repository/project.ts
```typescript
import { PrismaClient } from '@prisma/client'
import { Project } from '@shared/domain/project'

export class ProjectRepository {
 private prisma = new PrismaClient()

 async create(project: Omit<Project, 'id'>): Promise<Project> {
 return this.prisma.project.create({
 data: project
 })
 }

 async findById(id: string): Promise<Project | null> {
 return this.prisma.project.findUnique({
 where: { id }
 })
 }

 async findMany(options: {
 page: number
 limit: number
 }): Promise<Project[]> {
 const skip = (options.page - 1) * options.limit
 return this.prisma.project.findMany({
 skip,
 take: options.limit
 })
 }

 async update(id: string, data: Partial<Project>): Promise<Project> {
 return this.prisma.project.update({
 where: { id },
 data
 })
 }

 async delete(id: string): Promise<Project> {
 return this.prisma.project.delete({
 where: { id }
 })
 }
}
```

// FILE: monorepo/apps/api/src/service/auth.ts
```typescript
import { v4 as uuidv4 } from 'uuid'
import { User } from '@shared/domain/user'
import { UserRepository } from '@shared/repository/user'
import { AuthError } from '@shared/error/auth'

export class AuthService {
 constructor(private userRepo: UserRepository) {}

 async register(userData: Omit<User, 'id'>): Promise<User> {
 const existingUser = await this.userRepo.findByEmail(userData.email)
 if (existingUser) {
 throw new AuthError('Email already in use')
 }

 const hashedPassword = await this.userRepo.hashPassword(userData.password)
 const user = await this.userRepo.create({
 ...userData,
 password: hashedPassword,
 role: 'viewer'
 })

 return user
 }

 async login(credentials: { email: string; password: string }): Promise<{
 accessToken: string
 refreshToken: string
 }> {
 const user = await this.userRepo.findByEmail(credentials.email)
 if (!user) {
 throw new AuthError('Invalid credentials')
 }

 const isValidPassword = await this.userRepo.verifyPassword(
 credentials.password,
 user.password
 )
 if (!isValidPassword) {
 throw new AuthError('Invalid credentials')
 }

 const accessToken = this.generateAccessToken(user)
 const refreshToken = this.generateRefreshToken(user)

 return { accessToken, refreshToken }
 }

 async refresh(refreshToken: string): Promise<{
 accessToken: string
 newRefreshToken: string
 }> {
 // In a real application, you would verify the refresh token
 // and check if it's still valid
 const accessToken = this.generateAccessToken({ id: 'temp', role: 'viewer' })
 const newRefreshToken = this.generateRefreshToken({ id: 'temp', role: 'viewer' })

 return { accessToken, newRefreshToken }
 }

 async invalidateRefreshToken(refreshToken: string): Promise<void> {
 // In a real application, you would invalidate the refresh token
 // by marking it as used or storing it in a blacklist
 }

 private generateAccessToken(user: User): string {
 return `access_${uuidv4()}_${user.id}`
 }

 private generateRefreshToken(user: User): string {
 return `refresh_${uuidv4()}_${user.id}`
 }
}
```

// FILE: monorepo/apps/api/src/service/user.ts
```typescript
import { User } from '@shared/domain/user'
import { UserRepository } from '@shared/repository/user'
import { UserError } from '@shared/error/user'

export class UserService {
 constructor(private userRepo: UserRepository) {}

 async create(userData: Omit<User, 'id'>): Promise<User> {
 const existingUser = await this.userRepo.findByEmail(userData.email)
 if (existingUser) {
 throw new UserError('Email already in use')
 }

 const hashedPassword = await this.userRepo.hashPassword(userData.password)
 const user = await this.userRepo.create({
 ...userData,
 password: hashedPassword
 })

 return user
 }

 async getAll(options: { page: number; limit: number }): Promise<User[]> {
 return this.userRepo.findMany(options)
 }

 async getById(id: string): Promise<User> {
 const user = await this.userRepo.findById(id)
 if (!user) {
 throw new UserError('User not found')
 }
 return user
 }

 async update(id: string, data: Partial<User>): Promise<User> {
 const user = await this.userRepo.findById(id)
 if (!user) {
 throw new UserError('User not found')
 }

 return this.userRepo.update(id, data)
 }

 async delete(id: string): Promise<void> {
 const user = await this.userRepo.findById(id)
 if (!user) {
 throw new UserError('User not found')
 }

 await this.userRepo.delete(id)
 }
}
```

// FILE: monorepo/apps/api/src/service/project.ts
```typescript
import { Project } from '@shared/domain/project'
import { ProjectRepository } from '@shared/repository/project'
import { ProjectError } from '@shared/error/project'

export class ProjectService {
 constructor(private projectRepo: ProjectRepository) {}

 async create(projectData: Omit<Project, 'id'>): Promise<Project> {
 const project = await this.projectRepo.create(projectData)
 return project
 }

 async getAll(options: { page: number; limit: number }): Promise<Project[]> {
 return this.projectRepo.findMany(options)
 }

 async getById(id: string): Promise<Project> {
 const project = await this.projectRepo.findById(id)
 if (!project) {
 throw new ProjectError('Project not found')
 }
 return project
 }

 async update(id: string, data: Partial<Project>): Promise<Project> {
 const project = await this.projectRepo.findById(id)
 if (!project) {
 throw new ProjectError('Project not found')
 }

 return this.projectRepo.update(id, data)
 }

 async delete(id: string): Promise<void> {
 const project = await this.projectRepo.findById(id)
 if (!project) {
 throw new ProjectError('Project not found')
 }

 await this.projectRepo.delete(id)
 }
}
```

// FILE: monorepo/apps/api/src/domain/user.ts
```typescript
export interface User {
 id: string
 name: string
 email: string
 password: string
 role: 'admin' | 'editor' | 'viewer'
}
```

// FILE: monorepo/apps/api/src/domain/project.ts
```typescript
export interface Project {
 id: string
 name: string
 description?: string
 ownerId: string
}
```

// FILE: monorepo/apps/api/src/domain/task.ts
```typescript
export interface Task {
 id: string
 title: string
 description?: string
 status: 'todo' | 'in-progress' | 'done'
 projectId: string
 createdAt: Date
 updatedAt: Date
}
```

// FILE: monorepo/apps/api/src/domain/comment.ts
```typescript
export interface Comment {
 id: string
 content: string
 taskId: string
 userId: string
 createdAt: Date
}
```

// FILE: monorepo/apps/api/src/routes/auth.ts
```typescript
import { Router } from 'express'
import { AuthService } from '../service/auth'
import { UserRepository } from '../repository/user'

const router = Router()
const userRepo = new UserRepository()
const authService = new AuthService(userRepo)

router.post('/register', async (req, res) => {
 try {
 const user = await authService.register(req.body)
 res.status(201).json(user)
 } catch (error) {
 res.status(400).json({ error: error.message })
 }
})

router.post('/login', async (req, res) => {
 try {
 const { accessToken, refreshToken } = await authService.login(req.body)
 res.json({ accessToken, refreshToken })
 } catch (error) {
 res.status(401).json({ error: error.message })
 }
})

export default router
```

// FILE: monorepo/apps/api/src/routes/projects.ts
```typescript
import { Router } from 'express'
import { ProjectService } from '../service/project'
import { ProjectRepository } from '../repository/project'
import { PermissionGuard } from '../middleware/permission'

const router = Router()
const projectRepo = new ProjectRepository()
const projectService = new ProjectService(projectRepo)

router.get('/', async (req, res) => {
 try {
 const projects = await projectService.getAll(req.query)
 res.json(projects)
 } catch (error) {
 res.status(500).json({ error: error.message })
 }
})

router.post('/', async (req, res) => {
 try {
 const project = await projectService.create(req.body)
 res.status(201).json(project)
 } catch (error) {
 res.status(400).json({ error: error.message })
 }
})

router.get('/:id', async (req, res) => {
 try {
 const project = await projectService.getById(req.params.id)
 res.json(project)
 } catch (error) {
 res.status(404).json({ error: error.message })
 }
})

router.put('/:id', async (req, res) => {
 try {
 await PermissionGuard.check(req, 'update_project', req.params.id)
 const project = await projectService.update(req.params.id, req.body)
 res.json(project)
 } catch (error) {
 res.status(403).json({ error: error.message })
 }
})

router.delete('/:id', async (req, res) => {
 try {
 await PermissionGuard.check(req, 'delete_project', req.params.id)
 await projectService.delete(req.params.id)
 res.status(204).end()
 } catch (error) {
 res.status(403).json({ error: error.message })
 }
})

export default router
```

// FILE: monorepo/apps/api/src/routes/users.ts
```typescript
import { Router } from 'express'
import { UserService } from '../service/user'
import { UserRepository } from '../repository/user'

const router = Router()
const userRepo = new UserRepository()
const userService = new UserService(userRepo)

router.get('/', async (req, res) => {
 try {
 const users = await userService.getAll(req.query)
 res.json(users)
 } catch (error) {
 res.status(500).json({ error: error.message })
 }
})

router.get('/:id', async (req, res) => {
 try {
 const user = await userService.getById(req.params.id)
 res.json(user)
 } catch (error) {
 res.status(404).json({ error: error.message })
 }
})

router.put('/:id', async (req, res) => {
 try {
 const user = await userService.update(req.params.id, req.body)
 res.json(user)
 } catch (error) {
 res.status(400).json({ error: error.message })
 }
})

router.delete('/:id', async (req, res) => {
 try {
 await userService.delete(req.params.id)
 res.status(204).end()
 } catch (error) {
 res.status(400).json({ error: error.message })
 }
})

export default router
```

// FILE: monorepo/apps/api/src/index.ts
```typescript
import express from 'express'
import cors from 'cors'
import authRoutes from './routes/auth'
import projectRoutes from './routes/projects'
import userRoutes from './routes/users'

const app = express()
const PORT = process.env.PORT || 3000

// Middleware
app.use(cors())
app.use(express.json())

// Routes
app.use('/api/auth', authRoutes)
app.use('/api/projects', projectRoutes)
app.use('/api/users', userRoutes)

// Health check endpoint
app.get('/health', (req, res) => {
 res.status(200).json({ status: 'ok' })
})

// Start server
app.listen(PORT, () => {
 console.log(`Server is running on port ${PORT}`)
})
```

This is a comprehensive implementation of a task management API with user authentication, project management, and basic CRUD operations. The code follows a clean 
architecture pattern with separate concerns for routes, services, repositories, and domain models. It includes proper error handling and permission checks.

To use this API, you would need to:

1. Set up a PostgreSQL database and configure Prisma
2. Install the required dependencies (express, cors, prisma, etc.)
3. Set up environment variables for database connection
4. Run the application with `npm start` or `npm run dev`

The API provides endpoints for:
- User registration and login
- Project creation, retrieval, updating, and deletion
- User management (with appropriate permissions)

You can extend this further by adding task management endpoints, comment functionality, and more sophisticated authentication and authorization mechanisms.
assistant: [[reply_to_current]]Güzel test olmuş — ama bu çıktı, verdiğin prompta göre **çok zayıf** kalmış.

**Model 1 Değerlendirme (adil, çoklu metrik):**

- **1) Prompta uyum (format + kapsam)**: **1/10**  
  - “Sadece kod” şartını bozup açıklama yazmış.  
  - 30+ dosya / 2500+ satır şartı karşılanmıyor.  
  - Monorepo kapsamı eksik (packages/shared, infra, CI, docker, testler vb. yok).

- **2) Mimari tutarlılık**: **2/10**  
  - Aynı projede hem **Fastify** hem **Express** karışmış.  
  - Katman isimleri/path alias’lar tutarsız (`@shared/...` importları ama dosyalar `apps/api/src/...` içinde).

- **3) Derlenebilirlik / çalışma olasılığı**: **1/10**  
  - Büyük ihtimalle direkt compile/run etmez.  
  - Örnek: `import { argon2id } from 'argon2'` hatalı kullanım, `const app = fastify` yanlış, plugin/type kullanımları kırık.

- **4) Güvenlik doğruluğu (auth, token, RBAC)**: **2/10**  
  - JWT akışı gerçekçi değil; token üretimi string concat.  
  - Refresh rotasyonu/invalidasyon gerçek implementasyon değil (yorum seviyesinde).  
  - Permission guard mantığı yüzeysel.

- **5) İstenen domain kapsamı (Projects/Tasks/Realtime/Optimistic Locking)**: **2/10**  
  - Task CRUD, status flow, version-based optimistic locking, websocket event publish eksik/yarım.

- **6) Observability + Ops (health/ready/metrics, audit, rate limit by user+IP)**: **3/10**  
  - Bazı parçalar var gibi ama bütüncül ve çalışır değil.

- **7) Test & CI/CD & Infra**: **0/10**  
  - 20+ test dosyası, GitHub Actions, Docker multi-stage, compose, seed/migration yok.

- **8) Kod kalitesi (strict TS, gerçek implementasyon, TODO/placeholder yok)**: **2/10**  
  - “Real application’da şöyle olurdu” tarzı placeholder yorumlar var; strict/production-grade hedefini karşılamıyor.

---

### Ağırlıklı toplam skor: **16/100**

**Süre/çıktı verimi:** 6:20 süreye göre bu kalite düşük; özellikle “uzun ve tam kapsamlı üretim” testinde başarısız sayılır.  
İstersen bir sonraki model için sana **aynı rubric’i JSON skor şablonu** olarak veririm; her modeli birebir aynı kriterle puanlayıp leaderboard çıkarırız.
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-06 23:53 GMT+1] Model 2, bunu da degerlendir:


// FILE: package.json
{
 "name": "monorepo-template",
 "version": "1.0.0",
 "private": true,
 "type": "module",
 "scripts": {
 "dev": "turbo run dev",
 "build": "turbo run build",
 "lint": "turbo run lint",
 "test": "vitest",
 "db:generate": "prisma generate --schema=apps/api/prisma/schema.prisma",
 "db:migrate": "prisma migrate dev --schema=apps/api/prisma/schema.prisma",
 "db:seed": "tsx apps/api/src/scripts/seed.ts"
 },
 "devDependencies": {
 "@biomejs/biome": "^1.8.3",
 "@types/node": "^22.5.4",
 "turbo": "^2.1.0",
 "typescript": "^5.6.2"
 },
 "engines": {
 "node": ">=22.0.0"
 }
}

// FILE: turbo.json
{
 "$schema": "https://turbo.build/schema.json",
 "globalDependencies": [".env"],
 "pipeline": {
 "build": {
 "outputs": ["dist/**"]
 },
 "lint": {},
 "test": {}
 }
}

// FILE: packages/shared/package.json
{
 "name": "@repo/shared",
 "version": "1.0.0",
 "type": "module",
 "exports": {
 "./types": "./src/types/index.ts",
 "./dto": "./src/dto/index.ts",
 "./constants": "./src/constants/index.ts"
 },
 "devDependencies": {
 "zod": "^3.23.8"
 }
}

// FILE: packages/shared/tsconfig.json
{
 "extends": "../../tsconfig.base.json",
 "compilerOptions": {
 "outDir": "dist",
 "declaration": true
 },
 "include": ["src/**/*"],
 "exclude": ["node_modules", "dist"]
}

// FILE: packages/shared/src/constants/index.ts
import { z } from 'zod';

export const ROLES = ['admin', 'editor', 'viewer'] as const;
export type Role = (typeof ROLES)[number];

export const STATUS_FLOW = [
 'todo',
 'in_progress',
 'blocked',
 'done'
] as const;

export const TASK_STATUS_TYPES = {
 TODOLIST: 0,
 IN_PROGRESS: 1,
 BLOCKED: 2,
 DONE: 3
};

export const PAGINATION_LIMITS = {
 MIN: 1,
 DEFAULT: 20,
 MAX: 100
};

// FILE: packages/shared/src/types/index.ts
import type { Role } from '../constants/index.js';

export interface UserRecord {
 id: string;
 email: string;
 name: string;
 role: Role;
}

export interface AuthResponse extends Record<string, any> {
 user: Partial<UserRecord>;
 access_token: string;
 refresh_token: string;
 token_type: 'Bearer';
 expires_in: number;
}

export interface AuditLogEntry {
 userId?: string;
 action: string;
 resourceType: string;
 resourceId?: string;
 oldValue?: any;
 newValue?: any;
 ip: string;
 userAgent: string;
}

// FILE: packages/shared/src/dto/project.ts
import { z } from 'zod';

export const createProjectSchema = z.object({
 name: z.string().min(1).max(100),
 description: z.string().optional(),
 ownerId: z.string().uuid()
});

export type CreateProjectInput = z.input<typeof createProjectSchema>;

export const updateProjectSchema = z.object({
 name: z.string().min(1).max(100).optional(),
 description: z.string().optional(),
 status: z.enum(['active', 'archived']).optional()
});

export type UpdateProjectInput = z.input<typeof updateProjectSchema>;

// FILE: packages/shared/src/dto/task.ts
import { z } from 'zod';

export const createTaskSchema = z.object({
 projectId: z.string().uuid(),
 title: z.string().min(1).max(500),
 description: z.string().max(2000),
 priority: z.enum(['low', 'medium', 'high']),
 status: z.enum(['todo', 'in_progress', 'blocked', 'done']).default('todo'),
 assigneeId: z.string().uuid().optional()
});

export type CreateTaskInput = z.input<typeof createTaskSchema>;

export const updateTaskSchema = z.object({
 title: z.string().min(1).max(500).optional(),
 description: z.string().max(2000).optional(),
 status: z.enum(['todo', 'in_progress', 'blocked', 'done']).optional(),
 priority: z.enum(['low', 'medium', 'high']).optional()
});

export type UpdateTaskInput = z.input<typeof updateTaskSchema>;

// FILE: apps/api/package.json
{
 "name": "@repo/app",
 "version": "1.0.0",
 "private": true,
 "type": "module",
 "scripts": {
 "dev": "tsx watch src/index.ts",
 "start": "node dist/index.js",
 "build": "tsup src/index.ts --format esm --dts",
 "lint": "biome lint",
 "test": "vitest run"
 },
 "dependencies": {
 "@repo/shared": "file:../../packages/shared",
 "fastify": "^5.1.0",
 "prisma": "^5.17.0",
 "pino": "^9.3.2",
 "argon2": "^0.31.7",
 "jsonwebtoken": "^9.0.2",
 "@fastify/cors": "^10.0.2",
 "@fastify/helmet": "^12.0.1",
 "@fastify/rate-limit": "^10.1.4",
 "@fastify/accepts": "^4.3.0",
 "ws": "^8.18.0"
 },
 "devDependencies": {
 "@types/jsonwebtoken": "^9.0.6",
 "@types/node": "^22.5.4",
 "@types/ws": "^8.5.12",
 "tsup": "^8.2.4"
 }
}

// FILE: apps/api/tsconfig.json
{
 "extends": "../../tsconfig.base.json",
 "compilerOptions": {
 "outDir": "dist",
 "rootDir": "src"
 },
 "include": ["src/**/*"],
 "exclude": ["node_modules", "dist"]
}

// FILE: apps/api/prisma/schema.prisma
generator client {
 provider = "prisma-client-js"
}

datasource db {
 provider = "postgresql"
 url = env("DATABASE_URL")
}

model User {
 id String @id @default(cuid())
 email String @unique
 name String
 password String
 role Role @db.VarChar
 projects Project[]
 tasks Task[]

 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
}

model Project {
 id String @id @default(cuid())
 name String
 description String?
 status Enum @default("active") // active | archived
 ownerId String
 owner User @relation(fields: [ownerId], references: [id])
 tasks Task[]

 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
}

model Task {
 id String @id @default(cuid())
 projectId String
 project Project @relation(fields: [projectId], references: [id])
 title String
 description String?
 status Enum @default("todo") // todo | in_progress | blocked | done
 priority Enum @default("medium") // low | medium | high
 
 version Int @default(1)
 
 assigneeId String?
 assignee User? @relation(fields: [assigneeId], references: [id])

 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
}

model AuditLog {
 id String @id @default(cuid())
 action String
 resourceType String
 resourceId String?
 oldValue Json?
 newValue Json?
 userId String
 user User @relation(fields: [userId], references: [id])
 ip String
 userAgent String

 createdAt DateTime @default(now())
 
 @@index([userId])
}

model RefreshToken {
 token String @id
 userId String
 expiresAt DateTime
 revokedAt DateTime?

 user User @relation(fields: [userId], references: [id], onDelete: Cascade)

 createdAt DateTime @default(now())
}

enum Role {
 ADMIN
 EDITOR
 VIEWER
}

enum TaskStatus {
 TODOLIST
 IN_PROGRESS
 BLOCKED
 DONE
}

// FILE: apps/api/src/index.ts
import fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import accepts from '@fastify/accepts';
import { prisma } from './lib/db.js';
import * as routes from './routes/index.js';
import * as middlewares from './middleware/index.js';
import { errorHandler } from './handlers/error.js';

const start = async () => {
 const app = fastify({
 logger: {
 level: process.env.LOG_LEVEL || 'info',
 transport: {
 target: 'pino-pretty',
 options: { translateTime: 'UTC' }
 }
 }
 });

 // Register Middlewares
 await app.register(rateLimit, {
 max: 100,
 timeWindow: '1 minute',
 keyGenerator: (req) => `${req.ip}`
 });
 
 await app.register(cors, {
 origin: true
 });

 await app.register(helmet);
 await app.register(middlewares.requestId);

 // Register Accepts for Content Negotiation
 await app.register(accepts, { 
 schema: false,
 defaults: { 'application/json': true }
 });

 // Error Handling
 app.setErrorHandler(errorHandler);

 // Register Routes
 await app.register(routes.auth, { prefix: '/auth' });
 await app.register(routes.projects, { prefix: '/projects' });
 await app.register(routes.tasks, { prefix: '/tasks' });

 // Health & Metrics
 app.get('/health', async () => ({ status: 'ok' }));
 
 await prisma.$connect();
 const readyRoute = app.get('/ready', async () => ({ status: 'ready' }));

 return app;
};

// FILE: apps/api/src/lib/db.ts
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient({
 log: process.env.NODE_ENV !== 'production' ? ['query'] : []
});

// FILE: apps/api/src/middleware/requestId.ts
export const requestId = async (fastify, request, reply) => {
 const id = Math.random().toString(36).substring(2);
 request.id = id;
 fastify.log.info(`${id} - ${request.method} ${request.url}`);
};

// FILE: apps/api/src/middleware/auth.ts
import jwt from 'jsonwebtoken';
import { prisma } from '../lib/db.js';
import { ROLES, type Role } from '@repo/shared';

const SECRET_KEY = process.env.JWT_SECRET || 'dev-secret';
const REFRESH_SECRET = process.env.REFRESH_SECRET || 'dev-refresh-secret';

export const requireAuth = async (request) => {
 const header = request.headers.authorization;
 
 if (!header) return null;
 const token = header.split(' ')[1];

 try {
 const payload = jwt.verify(token, SECRET_KEY) as any; // TODO: Use proper typing
 const user = await prisma.user.findUnique({
 where: { id: payload.sub },
 select: ['id', 'email', 'emailVerified', 'name', ' schema: @relation(fields: [projectId], references: [id])
 
 status Enum @default("active")
 
 owner User @relation(fields:
assistant: [[reply_to_current]]Bu çıktı, **Model 1’den belirgin daha iyi** başlamış; ama yine production-grade kriterlerde ciddi kırıklar var.  
Ayrıca gönderdiğin içerik **yarım kesilmiş** (auth middleware ortasında bozuluyor), bu yüzden puanı “görünen kısım” üzerinden veriyorum.

### Model 2 – Çoklu Metrik Skor

- **1) Prompta uyum (format + kapsam): 4/10**  
  Dosya bazlı çıktı formatı iyi. Ama “sadece kod + devasa tam proje” hedefi için kapsam eksik/yarım.

- **2) Mimari tutarlılık: 6/10**  
  Monorepo + shared/api ayrımı var, Fastify seçimi tutarlı görünüyor. Bu kısım Model 1’den iyi.

- **3) Derlenebilirlik/çalıştırılabilirlik: 2/10**  
  Kritik hatalar var:
  - `start()` içinde `app.listen(...)` yok, `start()` çağrısı da görünmüyor.
  - `middleware/auth.ts` dosyası bozuk/truncated.
  - Prisma `select` kullanımı yanlış (`select: ['id', ...]` değil object olmalı).

- **4) Prisma/DB doğruluğu: 2/10**  
  - `status Enum` gibi tanımlar hatalı (`Enum` diye generic tip yok).
  - `TaskStatus` enum değerleri domainle uyumsuz (`TODOLIST` vs `todo`).
  - Role enum büyük harf, app tarafında küçük harf beklentisi var (potansiyel mapping sorunu).

- **5) Güvenlik & Auth: 3/10**  
  JWT iskeleti var ama incomplete. Refresh token, rotasyon, revoke akışı tam/sağlam görünmüyor.

- **6) Observability/Ops: 3/10**  
  `/health` ve `/ready` var; fakat `/metrics`, audit akışı, request-id implementasyonu zayıf.

- **7) Test/CI/Infra kapsamı: 1/10**  
  Görünen kısımda Vitest test dosyaları, GH Actions, Docker multi-stage, compose yok.

- **8) Uzun cevap / “yük testi” performansı: 5/10**  
  Model 1’e göre daha yapısal; ama hala “çok uzun, tam, çalışır” hedefinden uzak.

## Ağırlıklı toplam: **26/100**

### Kısa karşılaştırma
- **Model 1:** 16/100  
- **Model 2:** 26/100 → **daha iyi**, ama hâlâ başarısız sınıfta.

İstersen bir sonraki model için sana tek satırda uygulanabilir, objektif bir **hakem rubric’i (JSON template + otomatik puan formülü)** vereyim; her modele birebir aynı scoring’i yaparız.
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-06 23:56 GMT+1] Model 3:


// FILE: package.json
{
 "name": "enterprise-task-platform",
 "private": true,
 "workspaces": [
 "apps/*",
 "packages/*"
 ],
 "scripts": {
 "build": "tsc -b",
 "test": "vitest run",
 "lint": "eslint . --ext .ts",
 "typecheck": "tsc --noEmit",
 "dev": "pnpm --filter api dev"
 },
 "devDependencies": {
 "@types/node": "^22.0.0",
 "eslint": "^9.0.0",
 "typescript": "^5.4.0",
 "vitest": "^1.5.0"
 }
}

// FILE: tsconfig.base.json
{
 "compilerOptions": {
 "target": "ES2023",
 "module": "NodeNext",
 "moduleResolution": "NodeNext",
 "lib": ["ES2023"],
 "strict": true,
 "skipLibCheck": true,
 "resolveJsonModule": true,
 "esModuleInterop": true,
 "declaration": true,
 "sourceMap": true
 }
}

// FILE: apps/api/package.json
{
 "name": "api",
 "type": "module",
 "main": "dist/main.js",
 "scripts": {
 "dev": "tsx src/main.ts",
 "build": "tsc -p tsconfig.json",
 "start": "node dist/main.js",
 "test": "vitest"
 },
 "dependencies": {
 "@fastify/cors": "^9.0.0",
 "@fastify/helmet": "^12.0.0",
 "@fastify/jwt": "^8.0.0",
 "@fastify/rate-limit": "^9.0.0",
 "@fastify/swagger": "^9.0.0",
 "@fastify/websocket": "^9.0.0",
 "@prisma/client": "^5.14.0",
 "argon2": "^0.40.0",
 "fastify": "^4.27.0",
 "fastify-plugin": "^4.5.0",
 "ioredis": "^5.4.0",
 "pino": "^9.0.0",
 "prom-client": "^15.0.0",
 "uuid": "^9.0.0",
 "zod": "^3.23.0"
 },
 "devDependencies": {
 "prisma": "^5.14.0",
 "tsx": "^4.7.0",
 "vitest": "^1.5.0",
 "@types/uuid": "^9.0.0"
 }
}

// FILE: apps/api/tsconfig.json
{
 "extends": "../../tsconfig.base.json",
 "compilerOptions": {
 "outDir": "dist"
 },
 "include": ["src"]
}

// FILE: apps/api/src/main.ts
import { buildServer } from "./server.js";

async function main() {
 const server = await buildServer();
 await server.listen({ port: 3000, host: "0.0.0.0" });
}
main();

// FILE: apps/api/src/server.ts
import Fastify from "fastify";
import cors from "@fastify/cors";
import helmet from "@fastify/helmet";
import jwt from "@fastify/jwt";
import rateLimit from "@fastify/rate-limit";
import swagger from "@fastify/swagger";
import websocket from "@fastify/websocket";
import { registerRoutes } from "./routes/index.js";
import { requestId } from "./middleware/requestId.js";
import { errorHandler } from "./middleware/errorHandler.js";
import { metricsPlugin } from "./observability/metrics.js";

export async function buildServer() {
 const app = Fastify({
 logger: true
 });

 await app.register(cors);
 await app.register(helmet);
 await app.register(jwt, { secret: process.env.JWT_SECRET || "secret" });
 await app.register(rateLimit, { max: 100, timeWindow: "1 minute" });
 await app.register(swagger);
 await app.register(websocket);
 await app.register(metricsPlugin);

 app.addHook("onRequest", requestId);
 app.setErrorHandler(errorHandler);

 registerRoutes(app);

 return app;
}

// FILE: apps/api/src/routes/index.ts
import { FastifyInstance } from "fastify";
import { authRoutes } from "./auth.routes.js";
import { userRoutes } from "./user.routes.js";
import { projectRoutes } from "./project.routes.js";
import { taskRoutes } from "./task.routes.js";
import { healthRoutes } from "./health.routes.js";

export function registerRoutes(app: FastifyInstance) {
 app.register(authRoutes, { prefix: "/auth" });
 app.register(userRoutes, { prefix: "/users" });
 app.register(projectRoutes, { prefix: "/projects" });
 app.register(taskRoutes, { prefix: "/tasks" });
 app.register(healthRoutes);
}

// FILE: apps/api/src/routes/health.routes.ts
import { FastifyInstance } from "fastify";
import { register, collectDefaultMetrics } from "prom-client";

collectDefaultMetrics();

export async function healthRoutes(app: FastifyInstance) {
 app.get("/health", async () => ({ status: "ok" }));
 app.get("/ready", async () => ({ ready: true }));
 app.get("/metrics", async () => register.metrics());
}

// FILE: apps/api/src/routes/auth.routes.ts
import { FastifyInstance } from "fastify";
import { AuthController } from "../controllers/AuthController.js";

export async function authRoutes(app: FastifyInstance) {
 const controller = new AuthController();

 app.post("/register", controller.register);
 app.post("/login", controller.login);
 app.post("/refresh", controller.refresh);
 app.post("/logout", controller.logout);
 app.get("/me", { preHandler: [app.authenticate] }, controller.me);
}

// FILE: apps/api/src/routes/user.routes.ts
import { FastifyInstance } from "fastify";
import { UserController } from "../controllers/UserController.js";

export async function userRoutes(app: FastifyInstance) {
 const controller = new UserController();

 app.get("/", controller.list);
 app.post("/", controller.create);
 app.get("/:id", controller.get);
 app.put("/:id", controller.update);
 app.delete("/:id", controller.remove);
}

// FILE: apps/api/src/routes/project.routes.ts
import { FastifyInstance } from "fastify";
import { ProjectController } from "../controllers/ProjectController.js";

export async function projectRoutes(app: FastifyInstance) {
 const controller = new ProjectController();

 app.get("/", controller.list);
 app.post("/", controller.create);
 app.get("/:id", controller.get);
 app.put("/:id", controller.update);
 app.delete("/:id", controller.remove);
}

// FILE: apps/api/src/routes/task.routes.ts
import { FastifyInstance } from "fastify";
import { TaskController } from "../controllers/TaskController.js";

export async function taskRoutes(app: FastifyInstance) {
 const controller = new TaskController();

 app.get("/", controller.list);
 app.post("/", controller.create);
 app.get("/:id", controller.get);
 app.put("/:id", controller.update);
 app.delete("/:id", controller.remove);
}

// FILE: apps/api/src/controllers/AuthController.ts
import { FastifyReply, FastifyRequest } from "fastify";
import { AuthService } from "../services/AuthService.js";

export class AuthController {
 service = new AuthService();

 register = async (req: FastifyRequest, reply: FastifyReply) => {
 const user = await this.service.register(req.body as any);
 return reply.send(user);
 };

 login = async (req: FastifyRequest, reply: FastifyReply) => {
 const tokens = await this.service.login(req.body as any);
 return reply.send(tokens);
 };

 refresh = async (req: FastifyRequest, reply: FastifyReply) => {
 const tokens = await this.service.refresh(req.body as any);
 return reply.send(tokens);
 };

 logout = async () => ({ success: true });

 me = async (req: any) => req.user;
}

// FILE: apps/api/src/controllers/UserController.ts
import { FastifyRequest } from "fastify";
import { UserService } from "../services/UserService.js";

export class UserController {
 service = new UserService();

 list = async (req: FastifyRequest) => this.service.list(req.query as any);
 create = async (req: FastifyRequest) => this.service.create(req.body as any);
 get = async (req: FastifyRequest) =>
 this.service.get((req.params as any).id);
 update = async (req: FastifyRequest) =>
 this.service.update((req.params as any).id, req.body as any);
 remove = async (req: FastifyRequest) =>
 this.service.remove((req.params as any).id);
}

// FILE: apps/api/src/controllers/ProjectController.ts
import { FastifyRequest } from "fastify";
import { ProjectService } from "../services/ProjectService.js";

export class ProjectController {
 service = new ProjectService();

 list = async () => this.service.list();
 create = async (req: FastifyRequest) => this.service.create(req.body as any);
 get = async (req: FastifyRequest) =>
 this.service.get((req.params as any).id);
 update = async (req: FastifyRequest) =>
 this.service.update((req.params as any).id, req.body as any);
 remove = async (req: FastifyRequest) =>
 this.service.remove((req.params as any).id);
}

// FILE: apps/api/src/controllers/TaskController.ts
import { FastifyRequest } from "fastify";
import { TaskService } from "../services/TaskService.js";

export class TaskController {
 service = new TaskService();

 list = async () => this.service.list();
 create = async (req: FastifyRequest) => this.service.create(req.body as any);
 get = async (req: FastifyRequest) =>
 this.service.get((req.params as any).id);
 update = async (req: FastifyRequest) =>
 this.service.update((req.params as any).id, req.body as any);
 remove = async (req: FastifyRequest) =>
 this.service.remove((req.params as any).id);
}

// FILE: apps/api/src/services/AuthService.ts
import argon2 from "argon2";
import { prisma } from "../prisma/client.js";
import { signAccess, signRefresh } from "../utils/jwt.js";

export class AuthService {
 async register(data: any) {
 const hash = await argon2.hash(data.password);
 return prisma.user.create({
 data: { email: data.email, password: hash }
 });
 }

 async login(data: any) {
 const user = await prisma.user.findUnique({
 where: { email: data.email }
 });
 if (!user) throw new Error("invalid");

 const ok = await argon2.verify(user.password, data.password);
 if (!ok) throw new Error("invalid");

 return {
 accessToken: signAccess(user.id),
 refreshToken: signRefresh(user.id)
 };
 }

 async refresh(data: any) {
 return {
 accessToken: signAccess(data.userId),
 refreshToken: signRefresh(data.userId)
 };
 }
}

// FILE: apps/api/src/services/UserService.ts
import { prisma } from "../prisma/client.js";

export class UserService {
 list(query: any) {
 return prisma.user.findMany({
 skip: Number(query.offset) || 0,
 take: Number(query.limit) || 20
 });
 }

 create(data: any) {
 return prisma.user.create({ data });
 }

 get(id: string) {
 return prisma.user.findUnique({ where: { id } });
 }

 update(id: string, data: any) {
 return prisma.user.update({ where: { id }, data });
 }

 remove(id: string) {
 return prisma.user.delete({ where: { id } });
 }
}

// FILE: apps/api/src/services/ProjectService.ts
import { prisma } from "../prisma/client.js";

export class ProjectService {
 list() {
 return prisma.project.findMany();
 }

 create(data: any) {
 return prisma.project.create({ data });
 }

 get(id: string) {
 return prisma.project.findUnique({ where: { id } });
 }

 update(id: string, data: any) {
 return prisma.project.update({ where: { id }, data });
 }

 remove(id: string) {
 return prisma.project.delete({ where: { id } });
 }
}

// FILE: apps/api/src/services/TaskService.ts
import { prisma } from "../prisma/client.js";

export class TaskService {
 list() {
 return prisma.task.findMany();
 }

 create(data: any) {
 return prisma.task.create({ data });
 }

 get(id: string) {
 return prisma.task.findUnique({ where: { id } });
 }

 update(id: string, data: any) {
 return prisma.task.update({ where: { id }, data });
 }

 remove(id: string) {
 return prisma.task.delete({ where: { id } });
 }
}

// FILE: apps/api/src/prisma/client.ts
import { PrismaClient } from "@prisma/client";
export const prisma = new PrismaClient();

// FILE: apps/api/prisma/schema.prisma
generator client {
 provider = "prisma-client-js"
}

datasource db {
 provider = "postgresql"
 url = env("DATABASE_URL")
}

enum Role {
 ADMIN
 EDITOR
 VIEWER
}

enum TaskStatus {
 TODO
 IN_PROGRESS
 BLOCKED
 DONE
}

model User {
 id String @id @default(uuid())
 email String @unique
 password String
 role Role @default(VIEWER)
 projects Project[]
 tasks Task[]
 createdAt DateTime @default(now())
}

model Project {
 id String @id @default(uuid())
 name String
 ownerId String
 owner User @relation(fields: [ownerId], references: [id])
 tasks Task[]
 version Int @default(1)
 createdAt DateTime @default(now())
}

model Task {
 id String @id @default(uuid())
 title String
 status TaskStatus @default(TODO)
 projectId String
 project Project @relation(fields: [projectId], references: [id])
 assigneeId String?
 assignee User? @relation(fields: [assigneeId], references: [id])
 version Int @default(1)
 createdAt DateTime @default(now())
}

// FILE: apps/api/prisma/seed.ts
import { prisma } from "../src/prisma/client.js";
import argon2 from "argon2";

async function run() {
 const pass = await argon2.hash("password");

 const admin = await prisma.user.create({
 data: { email: "admin@test.com", password: pass, role: "ADMIN" }
 });

 const project = await prisma.project.create({
 data: { name: "Demo Project", ownerId: admin.id }
 });

 await prisma.task.createMany({
 data: [
 { title: "Setup repo", projectId: project.id },
 { title: "Write docs", projectId: project.id }
 ]
 });
}

run();

// FILE: apps/api/src/utils/jwt.ts
import jwt from "jsonwebtoken";

const secret = process.env.JWT_SECRET || "secret";

export function signAccess(userId: string) {
 return jwt.sign({ userId }, secret, { expiresIn: "15m" });
}

export function signRefresh(userId: string) {
 return jwt.sign({ userId }, secret, { expiresIn: "7d" });
}

// FILE: apps/api/src/middleware/errorHandler.ts
import { FastifyReply, FastifyRequest } from "fastify";

export function errorHandler(
 error: Error,
 _req: FastifyRequest,
 reply: FastifyReply
) {
 reply.status(500).send({ error: error.message });
}

// FILE: apps/api/src/middleware/requestId.ts
import { FastifyRequest } from "fastify";
import { v4 as uuid } from "uuid";

export function requestId(req: FastifyRequest, _reply: any, done: any) {
 req.headers["x-request-id"] = uuid();
 done();
}

// FILE: apps/api/src/observability/metrics.ts
import fp from "fastify-plugin";
import { Counter } from "prom-client";

const httpCounter = new Counter({
 name: "http_requests_total",
 help: "total http requests"
});

export const metricsPlugin = fp(async (app) => {
 app.addHook("onResponse", async () => {
 httpCounter.inc();
 });
});

// FILE: infra/Dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app .
CMD ["node","apps/api/dist/main.js"]

// FILE: infra/docker-compose.yml
version: "3.9"
services:
 db:
 image: postgres:16
 environment:
 POSTGRES_USER: postgres
 POSTGRES_PASSWORD: postgres
 POSTGRES_DB: tasks
 ports:
 - "5432:5432"

 redis:
 image: redis:7
 ports:
 - "6379:6379"

 api:
 build:
 context: ..
 dockerfile: infra/Dockerfile
 environment:
 DATABASE_URL: postgres://postgres:postgres@db:5432/tasks
 JWT_SECRET: secret
 ports:
 - "3000:3000"
 depends_on:
 - db
 - redis

// FILE: infra/.env.example
DATABASE_URL=postgres://postgres:postgres@localhost:5432/tasks
JWT_SECRET=supersecret
REDIS_URL=redis://localhost:6379

// FILE: .github/workflows/ci.yml
name: CI

on:
 push:
 branches: [ main ]

jobs:
 build:
 runs-on: ubuntu-latest

 steps:
 - uses: actions/checkout@v4

 - uses: actions/setup-node@v4
 with:
 node-version: 22

 - run: npm install
 - run: npm run typecheck
 - run: npm run lint
 - run: npm test
 - run: npm run build

// FILE: apps/api/tests/auth.test.ts
import { describe, it, expect } from "vitest";
import { AuthService } from "../src/services/AuthService.js";

describe("auth", () => {
 it("register", async () => {
 const service = new AuthService();
 const user = await service.register({
 email: "test@test.com",
 password: "123"
 });
 expect(user.email).toBe("test@test.com");
 });
});

// FILE: apps/api/tests/user.test.ts
import { describe, it, expect } from "vitest";
import { UserService } from "../src/services/UserService.js";

describe("users", () => {
 it("create user", async () => {
 const service = new UserService();
 const u = await service.create({ email: "a@a.com", password: "x" });
 expect(u.email).toBe("a@a.com");
 });
});

// FILE: apps/api/tests/project.test.ts
import { describe, it, expect } from "vitest";
import { ProjectService } from "../src/services/ProjectService.js";

describe("project", () => {
 it("create", async () => {
 const service = new ProjectService();
 const p = await service.create({ name: "p1", ownerId: "1" });
 expect(p.name).toBe("p1");
 });
});

// FILE: apps/api/tests/task.test.ts
import { describe, it, expect } from "vitest";
import { TaskService } from "../src/services/TaskService.js";

describe("task", () => {
 it("create", async () => {
 const service = new TaskService();
 const t = await service.create({ title: "task", projectId: "1" });
 expect(t.title).toBe("task");
 });
});

// FILE: packages/shared/package.json
{
 "name": "@shared",
 "version": "1.0.0",
 "type": "module",
 "main": "dist/index.js"
}

// FILE: packages/shared/src/index.ts
export * from "./roles.js";
export * from "./taskStatus.js";

// FILE: packages/shared/src/roles.ts
export type Role = "ADMIN" | "EDITOR" | "VIEWER";

// FILE: packages/shared/src/taskStatus.ts
export type TaskStatus = "TODO" | "IN_PROGRESS" | "BLOCKED" | "DONE";
assistant: [[reply_to_current]]Bu şimdiye kadarki en iyi aday, ama hâlâ “promptu tam karşıladı” seviyesinde değil.

### Model 3 – Çoklu Metrik Skor

- **1) Prompta uyum (format + kapsam): 6/10**  
  Dosya formatı düzgün, kapsam Model 1/2’den geniş. Ama hâlâ 2500+ satır, 20+ test dosyası, full production detayları eksik.

- **2) Mimari tutarlılık: 7/10**  
  Fastify + Prisma + katmanlı ayrım daha tutarlı. Monorepo niyeti net.  
  **Eksi:** `packages/shared/package.json` iki kez geliyor ve farklı isimlerle (`@repo/shared` vs `@shared`) çakışma.

- **3) Derlenebilirlik/çalıştırılabilirlik: 5/10**  
  Temel iskelet çalışabilir görünüyor.  
  **Kritik eksikler/hatalar:** `app.authenticate` tanımlı değil, bazı tipler `any`, refresh akışı yüzeysel, bazı import/export path’lerinde risk var.

- **4) Prisma/DB doğruluğu: 6/10**  
  Schema Model 2’den temiz. `version` alanları var.  
  **Eksi:** optimistic locking fiilen uygulanmamış (sadece kolon var), refresh token tablosu yok, audit log modeli yok.

- **5) Security & Auth: 5/10**  
  Argon2 + JWT var, rate limit var.  
  **Eksi:** gerçek refresh rotation/revocation yok, RBAC guard yok denecek kadar az, auth middleware zinciri incomplete.

- **6) Observability/Ops: 6/10**  
  `/health`, `/ready`, `/metrics` mevcut; request id ve error handler var.  
  **Eksi:** audit logging/structured request context daha zayıf.

- **7) Test/CI/Infra: 5/10**  
  CI + Docker + compose + seed var (iyi).  
  **Eksi:** testler az (4 dosya), mocking/integ/e2e derinliği düşük.

- **8) Kod kalitesi (strict TS, gerçek implementasyon): 5/10**  
  Genel kalite fena değil ama `any` ve yüzeysel servisler production-grade hedefi düşürüyor.

---

## Ağırlıklı toplam: **56/100**

### Şu ana kadar sıralama
1. **Model 3: 56/100**  
2. **Model 2: 26/100**  
3. **Model 1: 16/100**

Kısaca: **Model 3 açık ara önde**, ama hâlâ “tam istenen devasa, eksiksiz, production-ready” barını geçmiyor.  
İstersen bir sonraki model için aynı rubric’i tablo yerine tek satırlık “benchmark kartı” formatında verip çok hızlı karşılaştırma yapalım.
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-03-07 00:10 GMT+1] Model 4:


```json
// FILE: package.json
{
 "name": "enterprise-task-platform",
 "private": true,
 "version": "1.0.0",
 "packageManager": "pnpm@10.5.0",
 "scripts": {
 "build": "pnpm -r build",
 "dev": "pnpm --filter @acme/api dev",
 "lint": "pnpm -r lint",
 "typecheck": "pnpm -r typecheck",
 "test": "pnpm -r test",
 "test:coverage": "pnpm -r test:coverage",
 "db:generate": "pnpm --filter @acme/api prisma:generate",
 "db:migrate": "pnpm --filter @acme/api prisma:migrate",
 "db:seed": "pnpm --filter @acme/api prisma:seed"
 }
}
```

```yaml
// FILE: pnpm-workspace.yaml
packages:
 - "apps/*"
 - "packages/*"
 - "infra/*"
```

```json
// FILE: tsconfig.base.json
{
 "compilerOptions": {
 "target": "ES2022",
 "lib": ["ES2023"],
 "module": "NodeNext",
 "moduleResolution": "NodeNext",
 "verbatimModuleSyntax": true,
 "moduleDetection": "force",
 "strict": true,
 "skipLibCheck": true,
 "resolveJsonModule": true,
 "allowSyntheticDefaultImports": true,
 "noImplicitOverride": true,
 "noUncheckedIndexedAccess": true,
 "exactOptionalPropertyTypes": true,
 "forceConsistentCasingInFileNames": true,
 "esModuleInterop": true,
 "declaration": true,
 "sourceMap": true,
 "composite": true,
 "baseUrl": ".",
 "paths": {
 "@acme/shared": ["packages/shared/src/index.ts"],
 "@acme/shared/*": ["packages/shared/src/*"]
 }
 }
}
```

```dotenv
// FILE: .env.example
NODE_ENV=development
PORT=3000
HOST=0.0.0.0
LOG_LEVEL=info
DATABASE_URL=postgresql://postgres:postgres@db:5432/app?schema=public
REDIS_URL=redis://redis:6379
JWT_ACCESS_SECRET=super-access-secret
JWT_REFRESH_SECRET=super-refresh-secret
JWT_ACCESS_TTL=15m
JWT_REFRESH_TTL=30d
CORS_ORIGIN=http://localhost:3000
SWAGGER_ENABLED=true
METRICS_ENABLED=true
RATE_LIMIT_IP_MAX=120
RATE_LIMIT_USER_MAX=300
RATE_LIMIT_WINDOW_SEC=60
BCRYPT_ROUNDS=12
REQUEST_TIMEOUT_MS=30000
COOKIE_DOMAIN=localhost
```

```yaml
// FILE: docker-compose.yml
version: "3.9"

services:
 api:
 build:
 context: .
 dockerfile: infra/Dockerfile
 environment:
 NODE_ENV: development
 PORT: 3000
 HOST: 0.0.0.0
 LOG_LEVEL: info
 DATABASE_URL: postgresql://postgres:postgres@db:5432/app?schema=public
 REDIS_URL: redis://redis:6379
 JWT_ACCESS_SECRET: super-access-secret
 JWT_REFRESH_SECRET: super-refresh-secret
 JWT_ACCESS_TTL: 15m
 JWT_REFRESH_TTL: 30d
 CORS_ORIGIN: http://localhost:3000
 SWAGGER_ENABLED: "true"
 METRICS_ENABLED: "true"
 RATE_LIMIT_IP_MAX: 120
 RATE_LIMIT_USER_MAX: 300
 RATE_LIMIT_WINDOW_SEC: 60
 BCRYPT_ROUNDS: 12
 REQUEST_TIMEOUT_MS: 30000
 COOKIE_DOMAIN: localhost
 ports:
 - "3000:3000"
 depends_on:
 db:
 condition: service_healthy
 redis:
 condition: service_started
 command: sh -c "pnpm prisma migrate deploy && pnpm prisma db seed && node dist/apps/api/src/server.js"

 db:
 image: postgres:16-alpine
 environment:
 POSTGRES_DB: app
 POSTGRES_PASSWORD: postgres
 POSTGRES_USER: postgres
 ports:
 - "5432:5432"
 volumes:
 - postgres_data:/var/lib/postgresql/data
 healthcheck:
 test: ["CMD-SHELL", "pg_isready -U postgres -d app"]
 interval: 5s
 timeout: 5s
 retries: 20

 redis:
 image: redis:7-alpine
 ports:
 - "6379:6379"

volumes:
 postgres_data:
```

```dockerfile
// FILE: infra/Dockerfile
FROM node:22-alpine AS base
WORKDIR /app
RUN corepack enable

FROM base AS deps
COPY package.json pnpm-workspace.yaml tsconfig.base.json ./
COPY apps/api/package.json apps/api/package.json
COPY packages/shared/package.json packages/shared/package.json
RUN pnpm install --frozen-lockfile=false

FROM deps AS build
COPY . .
RUN pnpm --filter @acme/shared build
RUN pnpm --filter @acme/api prisma:generate
RUN pnpm --filter @acme/api build

FROM node:22-alpine AS runtime
WORKDIR /app
RUN corepack enable
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/pnpm-workspace.yaml ./pnpm-workspace.yaml
COPY --from=build /app/apps/api/package.json ./apps/api/package.json
COPY --from=build /app/apps/api/prisma ./apps/api/prisma
COPY --from=build /app/packages/shared/package.json ./packages/shared/package.json
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/apps/api/src/server.js"]
```

```yaml
// FILE: .github/workflows/ci.yml
name: ci

on:
 push:
 branches: ["main", "master"]
 pull_request:

jobs:
 build-test:
 runs-on: ubuntu-latest
 services:
 postgres:
 image: postgres:16
 env:
 POSTGRES_USER: postgres
 POSTGRES_PASSWORD: postgres
 POSTGRES_DB: app
 ports:
 - 5432:5432
 options: >-
 --health-cmd "pg_isready -U postgres -d app"
 --health-interval 10s
 --health-timeout 5s
 --health-retries 10
 redis:
 image: redis:7
 ports:
 - 6379:6379
 env:
 NODE_ENV: test
 PORT: 3000
 HOST: 127.0.0.1
 LOG_LEVEL: silent
 DATABASE_URL: postgresql://postgres:postgres@localhost:5432/app?schema=public
 REDIS_URL: redis://localhost:6379
 JWT_ACCESS_SECRET: ci-access-secret
 JWT_REFRESH_SECRET: ci-refresh-secret
 JWT_ACCESS_TTL: 15m
 JWT_REFRESH_TTL: 30d
 CORS_ORIGIN: http://localhost:3000
 SWAGGER_ENABLED: "true"
 METRICS_ENABLED: "true"
 RATE_LIMIT_IP_MAX: 1000
 RATE_LIMIT_USER_MAX: 1000
 RATE_LIMIT_WINDOW_SEC: 60
 BCRYPT_ROUNDS: 4
 REQUEST_TIMEOUT_MS: 10000
 COOKIE_DOMAIN: localhost
 steps:
 - uses: actions/checkout@v4
 - uses: pnpm/action-setup@v4
 with:
 version: 10.5.0
 - uses: actions/setup-node@v4
 with:
 node-version: 22
 cache: pnpm
 - run: pnpm install --frozen-lockfile=false
 - run: pnpm --filter @acme/api prisma:generate
 - run: pnpm --filter @acme/api prisma:migrate
 - run: pnpm lint
 - run: pnpm typecheck
 - run: pnpm test:coverage
 - run: pnpm build
```

```json
// FILE: packages/shared/package.json
{
 "name": "@acme/shared",
 "version": "1.0.0",
 "private": true,
 "type": "module",
 "main": "dist/index.js",
 "types": "dist/index.d.ts",
 "exports": {
 ".": {
 "types": "./dist/index.d.ts",
 "default": "./dist/index.js"
 }
 },
 "scripts": {
 "build": "tsc -p tsconfig.json",
 "lint": "tsc -p tsconfig.json --noEmit",
 "typecheck": "tsc -p tsconfig.json --noEmit",
 "test": "vitest run"
 },
 "dependencies": {
 "zod": "^3.24.2"
 },
 "devDependencies": {
 "typescript": "^5.7.3",
 "vitest": "^3.0.8"
 }
}
```

```json
// FILE: packages/shared/tsconfig.json
{
 "extends": "../../tsconfig.base.json",
 "compilerOptions": {
 "rootDir": "src",
 "outDir": "../../dist/packages/shared"
 },
 "include": ["src/**/*.ts"]
}
```

```typescript
// FILE: packages/shared/src/enums.ts
import { z } from "zod";

export const roleSchema = z.enum(["admin", "editor", "viewer"]);
export type Role = z.infer<typeof roleSchema>;

export const taskStatusSchema = z.enum(["todo", "in_progress", "blocked", "done"]);
export type TaskStatus = z.infer<typeof taskStatusSchema>;

export const sortOrderSchema = z.enum(["asc", "desc"]);
export type SortOrder = z.infer<typeof sortOrderSchema>;

export const userSortableFields = ["createdAt", "email", "name", "role"] as const;
export const projectSortableFields = ["createdAt", "updatedAt", "name"] as const;
export const taskSortableFields = ["createdAt", "updatedAt", "title", "status", "dueDate"] as const;
```

```typescript
// FILE: packages/shared/src/pagination.ts
import { z } from "zod";
import { sortOrderSchema } from "./enums.js";

export const pageQuerySchema = z.object({
 page: z.coerce.number().int().min(1).default(1),
 pageSize: z.coerce.number().int().min(1).max(100).default(20),
 sortBy: z.string().optional(),
 sortOrder: sortOrderSchema.default("desc")
});

export type PageQuery = z.infer<typeof pageQuerySchema>;

export type PageResult<T> = {
 items: T[];
 total: number;
 page: number;
 pageSize: number;
 pageCount: number;
};

export function toSkipTake(query: PageQuery): { skip: number; take: number } {
 return {
 skip: (query.page - 1) * query.pageSize,
 take: query.pageSize
 };
}

export function toPageResult<T>(items: T[], total: number, query: PageQuery): PageResult<T> {
 return {
 items,
 total,
 page: query.page,
 pageSize: query.pageSize,
 pageCount: Math.ceil(total / query.pageSize)
 };
}
```

```typescript
// FILE: packages/shared/src/errors.ts
export class AppError extends Error {
 public readonly statusCode: number;
 public readonly code: string;
 public readonly details?: unknown;

 public constructor(statusCode: number, code: string, message: string, details?: unknown) {
 super(message);
 this.name = "AppError";
 this.statusCode = statusCode;
 this.code = code;
 this.details = details;
 }
}

export class UnauthorizedError extends AppError {
 public constructor(message = "Unauthorized") {
 super(401, "UNAUTHORIZED", message);
 }
}

export class ForbiddenError extends AppError {
 public constructor(message = "Forbidden") {
 super(403, "FORBIDDEN", message);
 }
}

export class NotFoundError extends AppError {
 public constructor(message = "Not found") {
 super(404, "NOT_FOUND", message);
 }
}

export class ConflictError extends AppError {
 public constructor(message = "Conflict", details?: unknown) {
 super(409, "CONFLICT", message, details);
 }
}

export class ValidationAppError extends AppError {
 public constructor(message = "Validation failed", details?: unknown) {
 super(400, "VALIDATION_ERROR", message, details);
 }
}

export class RateLimitError extends AppError {
 public constructor(message = "Rate limit exceeded") {
 super(429, "RATE_LIMITED", message);
 }
}
```

```typescript
// FILE: packages/shared/src/contracts.ts
import { z } from "zod";
import { pageQuerySchema } from "./pagination.js";
import { roleSchema, taskStatusSchema, userSortableFields, projectSortableFields, taskSortableFields } from "./enums.js";

export const idParamSchema = z.object({
 id: z.string().uuid()
});

export const registerBodySchema = z.object({
 email: z.string().email(),
 password: z.string().min(8).max(128),
 name: z.string().min(2).max(120)
});

export const loginBodySchema = z.object({
 email: z.string().email(),
 password: z.string().min(8).max(128)
});

export const refreshBodySchema = z.object({
 refreshToken: z.string().min(20)
});

export const logoutBodySchema = z.object({
 refreshToken: z.string().min(20)
});

export const userFilterSchema = pageQuerySchema.extend({
 search: z.string().trim().optional(),
 role: roleSchema.optional(),
 sortBy: z.enum(userSortableFields).default("createdAt")
});

export const createUserBodySchema = z.object({
 email: z.string().email(),
 password: z.string().min(8).max(128),
 name: z.string().min(2).max(120),
 role: roleSchema.default("viewer")
});

export const updateUserBodySchema = z.object({
 email: z.string().email().optional(),
 name: z.string().min(2).max(120).optional(),
 role: roleSchema.optional(),
 password: z.string().min(8).max(128).optional(),
 version: z.number().int().min(1)
});

export const projectFilterSchema = pageQuerySchema.extend({
 search: z.string().trim().optional(),
 ownerId: z.string().uuid().optional(),
 sortBy: z.enum(projectSortableFields).default("updatedAt")
});

export const createProjectBodySchema = z.object({
 name: z.string().min(2).max(200),
 description: z.string().min(1).max(5000).optional(),
 ownerId: z.string().uuid()
});

export const updateProjectBodySchema = z.object({
 name: z.string().min(2).max(200).optional(),
 description: z.string().min(1).max(5000).nullable().optional(),
 ownerId: z.string().uuid().optional(),
 version: z.number().int().min(1)
});

export const taskFilterSchema = pageQuerySchema.extend({
 projectId: z.string().uuid().optional(),
 assigneeId: z.string().uuid().optional(),
 status: taskStatusSchema.optional(),
 search: z.string().trim().optional(),
 sortBy: z.enum(taskSortableFields).default("updatedAt")
});

export const createTaskBodySchema = z.object({
 projectId: z.string().uuid(),
 title: z.string().min(2).max(200),
 description: z.string().min(1).max(5000).optional(),
 assigneeId: z.string().uuid().nullable().optional(),
 status: taskStatusSchema.default("todo"),
 dueDate: z.string().datetime().nullable().optional()
});

export const updateTaskBodySchema = z.object({
 title: z.string().min(2).max(200).optional(),
 description: z.string().min(1).max(5000).nullable().optional(),
 assigneeId: z.string().uuid().nullable().optional(),
 status: taskStatusSchema.optional(),
 dueDate: z.string().datetime().nullable().optional(),
 version: z.number().int().min(1)
});

export const taskStatusTransitionSchema = z.object({
 status: taskStatusSchema,
 version: z.number().int().min(1)
});

export const userResponseSchema = z.object({
 id: z.string().uuid(),
 email: z.string().email(),
 name: z.string(),
 role: roleSchema,
 version: z.number().int(),
 createdAt: z.string(),
 updatedAt: z.string()
});

export const projectResponseSchema = z.object({
 id: z.string().uuid(),
 name: z.string(),
 description: z.string().nullable(),
 ownerId: z.string().uuid(),
 version: z.number().int(),
 createdAt: z.string(),
 updatedAt: z.string()
});

export const taskResponseSchema = z.object({
 id: z.string().uuid(),
 projectId: z.string().uuid(),
 title: z.string(),
 description: z.string().nullable(),
 assigneeId: z.string().uuid().nullable(),
 status: taskStatusSchema,
 version: z.number().int(),
 dueDate: z.string().nullable(),
 createdAt: z.string(),
 updatedAt: z.string()
});

export const authTokensResponseSchema = z.object({
 accessToken: z.string(),
 refreshToken: z.string()
});

export const authResponseSchema = z.object({
 user: userResponseSchema,
 tokens: authTokensResponseSchema
});

export const pageMetaSchema = z.object({
 total: z.number().int().nonnegative(),
 page: z.number().int().positive(),
 pageSize: z.number().int().positive(),
 pageCount: z.number().int().nonnegative()
});

export const pagedUsersResponseSchema = z.object({
 items: z.array(userResponseSchema),
 total: z.number().int().nonnegative(),
 page: z.number().int().positive(),
 pageSize: z.number().int().positive(),
 pageCount: z.number().int().nonnegative()
});

export const pagedProjectsResponseSchema = z.object({
 items: z.array(projectResponseSchema),
 total: z.number().int().nonnegative(),
 page: z.number().int().positive(),
 pageSize: z.number().int().positive(),
 pageCount: z.number().int().nonnegative()
});

export const pagedTasksResponseSchema = z.object({
 items: z.array(taskResponseSchema),
 total: z.number().int().nonnegative(),
 page: z.number().int().positive(),
 pageSize: z.number().int().positive(),
 pageCount: z.number().int().nonnegative()
});

export type RegisterBody = z.infer<typeof registerBodySchema>;
export type LoginBody = z.infer<typeof loginBodySchema>;
export type RefreshBody = z.infer<typeof refreshBodySchema>;
export type LogoutBody = z.infer<typeof logoutBodySchema>;
export type UserFilter = z.infer<typeof userFilterSchema>;
export type CreateUserBody = z.infer<typeof createUserBodySchema>;
export type UpdateUserBody = z.infer<typeof updateUserBodySchema>;
export type ProjectFilter = z.infer<typeof projectFilterSchema>;
export type CreateProjectBody = z.infer<typeof createProjectBodySchema>;
export type UpdateProjectBody = z.infer<typeof updateProjectBodySchema>;
export type TaskFilter = z.infer<typeof taskFilterSchema>;
export type CreateTaskBody = z.infer<typeof createTaskBodySchema>;
export type UpdateTaskBody = z.infer<typeof updateTaskBodySchema>;
export type TaskStatusTransition = z.infer<typeof taskStatusTransitionSchema>;
```

```typescript
// FILE: packages/shared/src/index.ts
export * from "./enums.js";
export * from "./pagination.js";
export * from "./errors.js";
export * from "./contracts.js";
```

```json
// FILE: apps/api/package.json
{
 "name": "@acme/api",
 "version": "1.0.0",
 "private": true,
 "type": "module",
 "main": "dist/apps/api/src/server.js",
 "types": "dist/apps/api/src/server.d.ts",
 "scripts": {
 "build": "tsc -p tsconfig.json",
 "dev": "tsx watch src/server.ts",
 "start": "node dist/apps/api/src/server.js",
 "lint": "tsc -p tsconfig.json --noEmit",
 "typecheck": "tsc -p tsconfig.json --noEmit",
 "test": "vitest run",
 "test:coverage": "vitest run --coverage",
 "prisma:generate": "prisma generate",
 "prisma:migrate": "prisma migrate deploy",
 "prisma:seed": "prisma db seed"
 },
 "prisma": {
 "seed": "tsx prisma/seed.ts"
 },
 "dependencies": {
 "@acme/shared": "workspace:*",
 "@fastify/cors": "^11.0.1",
 "@fastify/helmet": "^13.0.1",
 "@fastify/swagger": "^9.5.1",
 "@fastify/swagger-ui": "^5.2.1",
 "@fastify/websocket": "^11.0.1",
 "@prisma/client": "^6.4.1",
 "argon2": "^0.41.1",
 "bullmq": "^5.40.3",
 "dotenv": "^16.4.7",
 "fastify": "^5.2.1",
 "fastify-plugin": "^5.0.1",
 "fastify-type-provider-zod": "^4.0.2",
 "ioredis": "^5.4.2",
 "jsonwebtoken": "^9.0.2",
 "pino": "^9.6.0",
 "prom-client": "^15.1.3",
 "uuid": "^11.1.0",
 "zod": "^3.24.2"
 },
 "devDependencies": {
 "@types/jsonwebtoken": "^9.0.9",
 "@types/node": "^22.13.10",
 "@vitest/coverage-v8": "^3.0.8",
 "prisma": "^6.4.1",
 "tsx": "^4.19.3",
 "typescript": "^5.7.3",
 "vitest": "^3.0.8"
 }
}
```

```json
// FILE: apps/api/tsconfig.json
{
 "extends": "../../tsconfig.base.json",
 "compilerOptions": {
 "rootDir": "../..",
 "outDir": "../../dist",
 "types": ["node", "vitest/globals"]
 },
 "include": ["src/**/*.ts", "prisma/**/*.ts", "tests/**/*.ts"]
}
```

```typescript
// FILE: apps/api/vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
 test: {
 environment: "node",
 globals: true,
 include: ["tests/**/*.test.ts"],
 coverage: {
 provider: "v8",
 reporter: ["text", "lcov", "html"],
 include: ["src/**/*.ts", "../../packages/shared/src/**/*.ts"]
 }
 }
});
```

```prisma
// FILE: apps/api/prisma/schema.prisma
generator client {
 provider = "prisma-client-js"
}

datasource db {
 provider = "postgresql"
 url = env("DATABASE_URL")
}

enum Role {
 admin
 editor
 viewer
}

enum TaskStatus {
 todo
 in_progress
 blocked
 done
}

enum AuditAction {
 register
 login
 refresh
 logout
 create
 update
 delete
 read
 transition
}

model User {
 id String @id @default(uuid())
 email String @unique
 passwordHash String
 name String
 role Role @default(viewer)
 version Int @default(1)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 sessions Session[]
 ownedProjects Project[] @relation("ProjectOwner")
 assignedTasks Task[] @relation("TaskAssignee")
 auditLogs AuditLog[]
}

model Session {
 id String @id @default(uuid())
 userId String
 refreshTokenHash String
 userAgent String?
 ip String?
 expiresAt DateTime
 revokedAt DateTime?
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 user User @relation(fields: [userId], references: [id], onDelete: Cascade)

 @@index([userId])
 @@index([expiresAt])
}

model Project {
 id String @id @default(uuid())
 name String
 description String?
 ownerId String
 version Int @default(1)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 owner User @relation("ProjectOwner", fields: [ownerId], references: [id], onDelete: Restrict)
 tasks Task[]

 @@index([ownerId])
 @@unique([ownerId, name])
}

model Task {
 id String @id @default(uuid())
 projectId String
 title String
 description String?
 assigneeId String?
 status TaskStatus @default(todo)
 dueDate DateTime?
 version Int @default(1)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 project Project @relation(fields: [projectId], references: [id], onDelete: Cascade)
 assignee User? @relation("TaskAssignee", fields: [assigneeId], references: [id], onDelete: SetNull)

 @@index([projectId])
 @@index([assigneeId])
 @@index([status])
}

model AuditLog {
 id String @id @default(uuid())
 actorId String?
 actorEmail String?
 entityType String
 entityId String?
 action AuditAction
 metadata Json?
 ip String?
 createdAt DateTime @default(now())
 actor User? @relation(fields: [actorId], references: [id], onDelete: SetNull)

 @@index([actorId])
 @@index([entityType, entityId])
 @@index([createdAt])
}
```

```typescript
// FILE: apps/api/prisma/seed.ts
import { PrismaClient, Role, TaskStatus } from "@prisma/client";
import argon2 from "argon2";

const prisma = new PrismaClient();

async function main(): Promise<void> {
 await prisma.auditLog.deleteMany();
 await prisma.task.deleteMany();
 await prisma.project.deleteMany();
 await prisma.session.deleteMany();
 await prisma.user.deleteMany();

 const passwordHash = await argon2.hash("Password123!");

 const [admin, editor, viewer, manager] = await Promise.all([
 prisma.user.create({
 data: {
 email: "admin@example.com",
 passwordHash,
 name: "Aylin Admin",
 role: Role.admin
 }
 }),
 prisma.user.create({
 data: {
 email: "editor@example.com",
 passwordHash,
 name: "Emre Editor",
 role: Role.editor
 }
 }),
 prisma.user.create({
 data: {
 email: "viewer@example.com",
 passwordHash,
 name: "Veli Viewer",
 role: Role.viewer
 }
 }),
 prisma.user.create({
 data: {
 email: "manager@example.com",
 passwordHash,
 name: "Maya Manager",
 role: Role.editor
 }
 })
 ]);

 const projectData = [
 {
 name: "Phoenix CRM Modernization",
 description: "Sales workflows migration to event-driven architecture.",
 ownerId: admin.id
 },
 {
 name: "Mercury Mobile Platform",
 description: "Shared backend capabilities for mobile clients.",
 ownerId: manager.id
 },
 {
 name: "Atlas Analytics",
 description: "Operational reporting and realtime dashboards.",
 ownerId: editor.id
 }
 ];

 const projects = [];
 for (const data of projectData) {
 projects.push(await prisma.project.create({ data }));
 }

 const realisticTasks = [
 {
 projectId: projects[0]!.id,
 title: "Design customer aggregate",
 description: "Establish write model boundaries and event contracts.",
 assigneeId: admin.id,
 status: TaskStatus.in_progress,
 dueDate: new Date(Date.now() + 4 * 86400000)
 },
 {
 projectId: projects[0]!.id,
 title: "Implement lead deduplication rule engine",
 description: "Create deterministic merge strategy with auditability.",
 assigneeId: editor.id,
 status: TaskStatus.todo,
 dueDate: new Date(Date.now() + 8 * 86400000)
 },
 {
 projectId: projects[1]!.id,
 title: "Provision websocket gateway",
 description: "Broadcast task updates to mobile clients with auth context.",
 assigneeId: manager.id,
 status: TaskStatus.blocked,
 dueDate: new Date(Date.now() + 2 * 86400000)
 },
 {
 projectId: projects[1]!.id,
 title: "Define refresh token rotation policy",
 description: "Ensure secure mobile session continuity and revocation.",
 assigneeId: admin.id,
 status: TaskStatus.done,
 dueDate: new Date(Date.now() - 3 * 86400000)
 },
 {
 projectId: projects[2]!.id,
 title: "Model dashboard latency metrics",
 description: "Publish histogram and percentile series for API latency.",
 assigneeId: editor.id,
 status: TaskStatus.in_progress,
 dueDate: new Date(Date.now() + 5 * 86400000)
 },
 {
 projectId: projects[2]!.id,
 title: "Seed trial tenant data",
 description: "Create realistic analytics fixture data for product demos.",
 assigneeId: viewer.id,
 status: TaskStatus.todo,
 dueDate: new Date(Date.now() + 10 * 86400000)
 }
 ];

 for (const task of realisticTasks) {
 await prisma.task.create({ data: task });
 }

 await prisma.auditLog.createMany({
 data: [
 {
 actorId: admin.id,
 actorEmail: admin.email,
 entityType: "seed",
 entityId: projects[0]!.id,
 action: "create",
 metadata: { note: "Seeded project" },
 ip: "127.0.0.1"
 },
 {
 actorId: manager.id,
 actorEmail: manager.email,
 entityType: "seed",
 entityId: projects[1]!.id,
 action: "create",
 metadata: { note: "Seeded project" },
 ip: "127.0.0.1"
 }
 ]
 });
}

main()
 .then(async () => {
 await prisma.$disconnect();
 })
 .catch(async (error: unknown) => {
 console.error(error);
 await prisma.$disconnect();
 process.exit(1);
 });
```

```typescript
// FILE: apps/api/src/types/fastify.d.ts
import "fastify";
import type { PrismaClient } from "@prisma/client";
import type Redis from "ioredis";
import type { Queue } from "bullmq";
import type { JwtClaims } from "../auth/jwt.js";
import type { AppEnv } from "../config/env.js";
import type { RealtimeHub } from "../realtime/hub.js";

declare module "fastify" {
 interface FastifyInstance {
 prisma: PrismaClient;
 redis: Redis;
 env: AppEnv;
 auditQueue: Queue;
 realtimeQueue: Queue;
 realtimeHub: RealtimeHub;
 metrics: {
 register: import("prom-client").Registry;
 httpRequestDurationMs: import("prom-client").Histogram<string>;
 httpRequestCounter: import("prom-client").Counter<string>;
 authFailureCounter: import("prom-client").Counter<string>;
 };
 }

 interface FastifyRequest {
 requestId: string;
 auth?: JwtClaims;
 }
}
```

```typescript
// FILE: apps/api/src/config/env.ts
import dotenv from "dotenv";
import { z } from "zod";

dotenv.config();

const envSchema = z.object({
 NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
 PORT: z.coerce.number().int().positive().default(3000),
 HOST: z.string().min(1).default("0.0.0.0"),
 LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace", "silent"]).default("info"),
 DATABASE_URL: z.string().min(1),
 REDIS_URL: z.string().url(),
 JWT_ACCESS_SECRET: z.string().min(16),
 JWT_REFRESH_SECRET: z.string().min(16),
 JWT_ACCESS_TTL: z.string().min(2).default("15m"),
 JWT_REFRESH_TTL: z.string().min(2).default("30d"),
 CORS_ORIGIN: z.string().min(1),
 SWAGGER_ENABLED: z.coerce.boolean().default(true),
 METRICS_ENABLED: z.coerce.boolean().default(true),
 RATE_LIMIT_IP_MAX: z.coerce.number().int().positive().default(120),
 RATE_LIMIT_USER_MAX: z.coerce.number().int().positive().default(300),
 RATE_LIMIT_WINDOW_SEC: z.coerce.number().int().positive().default(60),
 BCRYPT_ROUNDS: z.coerce.number().int().positive().default(12),
 REQUEST_TIMEOUT_MS: z.coerce.number().int().positive().default(30000),
 COOKIE_DOMAIN: z.string().min(1).default("localhost")
});

export type AppEnv = z.infer<typeof envSchema>;

export const env: AppEnv = envSchema.parse(process.env);
```

```typescript
// FILE: apps/api/src/lib/logger.ts
import pino from "pino";
import { env } from "../config/env.js";

export const logger = pino({
 level: env.LOG_LEVEL,
 transport:
 env.NODE_ENV === "development"
 ? {
 target: "pino/file",
 options: { destination: 1 }
 }
 : undefined,
 redact: {
 paths: ["req.headers.authorization", "req.headers.cookie", "password", "refreshToken"],
 censor: "[REDACTED]"
 }
});
```

```typescript
// FILE: apps/api/src/lib/metrics.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import client from "prom-client";

const metricsPlugin: FastifyPluginAsync = fp(async (fastify) => {
 const register = new client.Registry();
 client.collectDefaultMetrics({ register });

 const httpRequestDurationMs = new client.Histogram({
 name: "http_request_duration_ms",
 help: "HTTP request duration in milliseconds",
 labelNames: ["method", "route", "status_code"]
 });

 const httpRequestCounter = new client.Counter({
 name: "http_requests_total",
 help: "Total HTTP requests",
 labelNames: ["method", "route", "status_code"]
 });

 const authFailureCounter = new client.Counter({
 name: "auth_failures_total",
 help: "Authentication failures",
 labelNames: ["reason"]
 });

 register.registerMetric(httpRequestDurationMs);
 register.registerMetric(httpRequestCounter);
 register.registerMetric(authFailureCounter);

 fastify.decorate("metrics", {
 register,
 httpRequestDurationMs,
 httpRequestCounter,
 authFailureCounter
 });

 fastify.addHook("onRequest", async (request) => {
 (request as FastifyRequest & { __startTime?: number }).__startTime = performance.now();
 });

 fastify.addHook("onResponse", async (request, reply) => {
 const route = request.routeOptions.url || request.routerPath || request.url;
 const status = String(reply.statusCode);
 const start = (request as FastifyRequest & { __startTime?: number }).__startTime ?? performance.now();
 const duration = performance.now() - start;
 fastify.metrics.httpRequestDurationMs.labels(request.method, route, status).observe(duration);
 fastify.metrics.httpRequestCounter.labels(request.method, route, status).inc();
 });

 fastify.get("/metrics", async (_request, reply) => {
 const payload = await register.metrics();
 reply.header("Content-Type", register.contentType);
 return payload;
 });
});

export default metricsPlugin;
```

```typescript
// FILE: apps/api/src/lib/errors.ts
import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";
import { AppError } from "@acme/shared";
import { ZodError } from "zod";

export function errorHandler(error: FastifyError | Error, request: FastifyRequest, reply: FastifyReply): void {
 request.log.error({ err: error }, "request_failed");

 if (error instanceof AppError) {
 reply.status(error.statusCode).send({
 error: {
 code: error.code,
 message: error.message,
 details: error.details ?? null,
 requestId: request.requestId
 }
 });
 return;
 }

 if (error instanceof ZodError) {
 reply.status(400).send({
 error: {
 code: "VALIDATION_ERROR",
 message: "Validation failed",
 details: error.flatten(),
 requestId: request.requestId
 }
 });
 return;
 }

 const statusCode = "statusCode" in error && typeof error.statusCode === "number" ? error.statusCode : 500;
 reply.status(statusCode).send({
 error: {
 code: statusCode >= 500 ? "INTERNAL_SERVER_ERROR" : "REQUEST_ERROR",
 message: error.message || "Internal server error",
 details: null,
 requestId: request.requestId
 }
 });
}
```

```typescript
// FILE: apps/api/src/utils/ids.ts
import { randomUUID } from "node:crypto";

export function createRequestId(): string {
 return randomUUID();
}
```

```typescript
// FILE: apps/api/src/utils/time.ts
export function addMs(date: Date, ms: number): Date {
 return new Date(date.getTime() + ms);
}

export function parseDurationToMs(input: string): number {
 const value = Number.parseInt(input.slice(0, -1), 10);
 const unit = input.slice(-1);

 if (Number.isNaN(value)) {
 throw new Error(`Invalid duration: ${input}`);
 }

 switch (unit) {
 case "s":
 return value * 1000;
 case "m":
 return value * 60_000;
 case "h":
 return value * 3_600_000;
 case "d":
 return value * 86_400_000;
 default:
 throw new Error(`Unsupported duration unit: ${input}`);
 }
}
```

```typescript
// FILE: apps/api/src/auth/password.ts
import argon2 from "argon2";

export async function hashPassword(password: string): Promise<string> {
 return argon2.hash(password);
}

export async function verifyPassword(hash: string, password: string): Promise<boolean> {
 return argon2.verify(hash, password);
}
```

```typescript
// FILE: apps/api/src/auth/jwt.ts
import jwt from "jsonwebtoken";
import type { Role } from "@acme/shared";
import { env } from "../config/env.js";

export type JwtClaims = {
 sub: string;
 email: string;
 role: Role;
 type: "access" | "refresh";
 sessionId: string;
};

export function signAccessToken(claims: Omit<JwtClaims, "type">): string {
 return jwt.sign(
 {
 ...claims,
 type: "access"
 },
 env.JWT_ACCESS_SECRET,
 {
 expiresIn: env.JWT_ACCESS_TTL
 }
 );
}

export function signRefreshToken(claims: Omit<JwtClaims, "type">): string {
 return jwt.sign(
 {
 ...claims,
 type: "refresh"
 },
 env.JWT_REFRESH_SECRET,
 {
 expiresIn: env.JWT_REFRESH_TTL
 }
 );
}

export function verifyAccessToken(token: string): JwtClaims {
 return jwt.verify(token, env.JWT_ACCESS_SECRET) as JwtClaims;
}

export function verifyRefreshToken(token: string): JwtClaims {
 return jwt.verify(token, env.JWT_REFRESH_SECRET) as JwtClaims;
}
```

```typescript
// FILE: apps/api/src/realtime/hub.ts
import type { SocketStream } from "@fastify/websocket";
import type { FastifyRequest } from "fastify";

type SubscriptionEvent =
 | { type: "task.updated"; payload: Record<string, unknown> }
 | { type: "task.created"; payload: Record<string, unknown> }
 | { type: "task.deleted"; payload: Record<string, unknown> };

type ClientContext = {
 id: string;
 socket: SocketStream["socket"];
 request: FastifyRequest;
};

export class RealtimeHub {
 private readonly clients = new Map<string, ClientContext>();

 public addClient(client: ClientContext): void {
 this.clients.set(client.id, client);
 client.socket.on("close", () => {
 this.clients.delete(client.id);
 });
 }

 public removeClient(id: string): void {
 this.clients.delete(id);
 }

 public broadcast(event: SubscriptionEvent): void {
 const payload = JSON.stringify(event);
 for (const client of this.clients.values()) {
 if (client.socket.readyState === 1) {
 client.socket.send(payload);
 }
 }
 }

 public size(): number {
 return this.clients.size;
 }
}
```

```typescript
// FILE: apps/api/src/plugins/prisma.ts
import fp from "fastify-plugin";
import { PrismaClient } from "@prisma/client";
import type { FastifyPluginAsync } from "fastify";

const prismaPlugin: FastifyPluginAsync = fp(async (fastify) => {
 const prisma = new PrismaClient({
 log: ["error", "warn"]
 });

 await prisma.$connect();
 fastify.decorate("prisma", prisma);

 fastify.addHook("onClose", async () => {
 await prisma.$disconnect();
 });
});

export default prismaPlugin;
```

```typescript
// FILE: apps/api/src/plugins/redis.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import Redis from "ioredis";
import { Queue, Worker } from "bullmq";
import { env } from "../config/env.js";

const redisPlugin: FastifyPluginAsync = fp(async (fastify) => {
 const redis = new Redis(env.REDIS_URL, { maxRetriesPerRequest: null });
 fastify.decorate("redis", redis);

 const auditQueue = new Queue("audit-log", {
 connection: redis
 });

 const realtimeQueue = new Queue("realtime-events", {
 connection: redis
 });

 fastify.decorate("auditQueue", auditQueue);
 fastify.decorate("realtimeQueue", realtimeQueue);

 const auditWorker = new Worker(
 "audit-log",
 async (job) => {
 const payload = job.data as {
 actorId?: string;
 actorEmail?: string;
 entityType: string;
 entityId?: string;
 action: "register" | "login" | "refresh" | "logout" | "create" | "update" | "delete" | "read" | "transition";
 metadata?: Record<string, unknown>;
 ip?: string;
 };
 await fastify.prisma.auditLog.create({
 data: {
 actorId: payload.actorId,
 actorEmail: payload.actorEmail,
 entityType: payload.entityType,
 entityId: payload.entityId,
 action: payload.action,
 metadata: payload.metadata,
 ip: payload.ip
 }
 });
 },
 {
 connection: redis,
 concurrency: 5
 }
 );

 const realtimeWorker = new Worker(
 "realtime-events",
 async (job) => {
 const payload = job.data as {
 type: "task.updated" | "task.created" | "task.deleted";
 data: Record<string, unknown>;
 };
 fastify.realtimeHub.broadcast({
 type: payload.type,
 payload: payload.data
 });
 },
 {
 connection: redis,
 concurrency: 10
 }
 );

 fastify.addHook("onClose", async () => {
 await Promise.all([auditWorker.close(), realtimeWorker.close(), auditQueue.close(), realtimeQueue.close(), redis.quit()]);
 });
});

export default redisPlugin;
```

```typescript
// FILE: apps/api/src/plugins/security.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import cors from "@fastify/cors";
import helmet from "@fastify/helmet";
import { env } from "../config/env.js";

function sanitizeString(value: string): string {
 return value.replace(/[<>]/g, "").trim();
}

function sanitizeUnknown(value: unknown): unknown {
 if (typeof value === "string") {
 return sanitizeString(value);
 }
 if (Array.isArray(value)) {
 return value.map(sanitizeUnknown);
 }
 if (value && typeof value === "object") {
 return Object.fromEntries(
 Object.entries(value).map(([key, val]) => [key, sanitizeUnknown(val)])
 );
 }
 return value;
}

const securityPlugin: FastifyPluginAsync = fp(async (fastify) => {
 await fastify.register(helmet);
 await fastify.register(cors, {
 origin: env.CORS_ORIGIN.split(",").map((v) => v.trim()),
 credentials: true
 });

 fastify.addHook("preValidation", async (request) => {
 request.body = sanitizeUnknown(request.body);
 request.query = sanitizeUnknown(request.query);
 request.params = sanitizeUnknown(request.params);
 });
});

export default securityPlugin;
```

```typescript
// FILE: apps/api/src/plugins/request-context.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import { createRequestId } from "../utils/ids.js";

const requestContextPlugin: FastifyPluginAsync = fp(async (fastify) => {
 fastify.addHook("onRequest", async (request, reply) => {
 const requestId = request.headers["x-request-id"]?.toString() || createRequestId();
 request.requestId = requestId;
 reply.header("x-request-id", requestId);
 });
});

export default requestContextPlugin;
```

```typescript
// FILE: apps/api/src/plugins/rate-limit.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import { RateLimitError } from "@acme/shared";
import { env } from "../config/env.js";

async function consume(redisKey: string, max: number, windowSec: number, redis: import("ioredis").default): Promise<void> {
 const current = await redis.incr(redisKey);
 if (current === 1) {
 await redis.expire(redisKey, windowSec);
 }
 if (current > max) {
 throw new RateLimitError();
 }
}

const rateLimitPlugin: FastifyPluginAsync = fp(async (fastify) => {
 fastify.addHook("preHandler", async (request) => {
 const ip = request.ip;
 await consume(`rl:ip:${ip}`, env.RATE_LIMIT_IP_MAX, env.RATE_LIMIT_WINDOW_SEC, fastify.redis);
 if (request.auth?.sub) {
 await consume(`rl:user:${request.auth.sub}`, env.RATE_LIMIT_USER_MAX, env.RATE_LIMIT_WINDOW_SEC, fastify.redis);
 }
 });
});

export default rateLimitPlugin;
```

```typescript
// FILE: apps/api/src/plugins/swagger.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import swagger from "@fastify/swagger";
import swaggerUi from "@fastify/swagger-ui";

const swaggerPlugin: FastifyPluginAsync = fp(async (fastify) => {
 if (!fastify.env.SWAGGER_ENABLED) {
 return;
 }

 await fastify.register(swagger, {
 openapi: {
 info: {
 title: "Enterprise Task Platform API",
 version: "1.0.0"
 },
 servers: [{ url: "/" }],
 components: {
 securitySchemes: {
 bearerAuth: {
 type: "http",
 scheme: "bearer",
 bearerFormat: "JWT"
 }
 }
 }
 }
 });

 await fastify.register(swaggerUi, {
 routePrefix: "/docs",
 uiConfig: {
 docExpansion: "list",
 deepLinking: false
 }
 });
});

export default swaggerPlugin;
```

```typescript
// FILE: apps/api/src/plugins/realtime.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import websocket from "@fastify/websocket";
import { randomUUID } from "node:crypto";
import { RealtimeHub } from "../realtime/hub.js";
import { verifyAccessToken } from "../auth/jwt.js";

const realtimePlugin: FastifyPluginAsync = fp(async (fastify) => {
 const hub = new RealtimeHub();
 fastify.decorate("realtimeHub", hub);

 await fastify.register(websocket);

 fastify.get("/ws", { websocket: true }, async (socket, request) => {
 const authHeader = request.headers.authorization;
 const token = authHeader?.startsWith("Bearer ") ? authHeader.slice(7) : undefined;
 if (!token) {
 socket.close(4001, "Unauthorized");
 return;
 }

 try {
 request.auth = verifyAccessToken(token);
 } catch {
 socket.close(4001, "Unauthorized");
 return;
 }

 const id = randomUUID();
 hub.addClient({ id, socket, request });

 socket.send(
 JSON.stringify({
 type: "connected",
 payload: {
 clientId: id
 }
 })
 );

 socket.on("message", (raw) => {
 socket.send(
 JSON.stringify({
 type: "ack",
 payload: {
 received: raw.toString()
 }
 })
 );
 });

 socket.on("close", () => {
 hub.removeClient(id);
 });
 });
});

export default realtimePlugin;
```

```typescript
// FILE: apps/api/src/middleware/authenticate.ts
import type { FastifyReply, FastifyRequest } from "fastify";
import { UnauthorizedError } from "@acme/shared";
import { verifyAccessToken } from "../auth/jwt.js";

export async function authenticate(request: FastifyRequest, _reply: FastifyReply): Promise<void> {
 const authorization = request.headers.authorization;
 const token = authorization?.startsWith("Bearer ") ? authorization.slice(7) : undefined;

 if (!token) {
 throw new UnauthorizedError("Missing bearer token");
 }

 try {
 request.auth = verifyAccessToken(token);
 } catch {
 request.server.metrics.authFailureCounter.labels("invalid_access_token").inc();
 throw new UnauthorizedError("Invalid access token");
 }
}
```

```typescript
// FILE: apps/api/src/middleware/authorize.ts
import type { FastifyReply, FastifyRequest } from "fastify";
import { ForbiddenError, type Role } from "@acme/shared";

export function authorize(...roles: Role[]) {
 return async function roleGuard(request: FastifyRequest, _reply: FastifyReply): Promise<void> {
 const role = request.auth?.role;
 if (!role || !roles.includes(role)) {
 throw new ForbiddenError();
 }
 };
}
```

```typescript
// FILE: apps/api/src/repositories/user.repository.ts
import type { Prisma, PrismaClient, User } from "@prisma/client";
import type { CreateUserBody, UpdateUserBody, UserFilter } from "@acme/shared";
import { toSkipTake } from "@acme/shared";

export class UserRepository {
 public constructor(private readonly prisma: PrismaClient) {}

 public create(data: CreateUserBody & { passwordHash: string }): Promise<User> {
 return this.prisma.user.create({
 data: {
 email: data.email,
 name: data.name,
 passwordHash: data.passwordHash,
 role: data.role
 }
 });
 }

 public findByEmail(email: string): Promise<User | null> {
 return this.prisma.user.findUnique({ where: { email } });
 }

 public findById(id: string): Promise<User | null> {
 return this.prisma.user.findUnique({ where: { id } });
 }

 public async findMany(filter: UserFilter): Promise<{ items: User[]; total: number }> {
 const where: Prisma.UserWhereInput = filter.search
 ? {
 OR: [
 { email: { contains: filter.search, mode: "insensitive" } },
 { name: { contains: filter.search, mode: "insensitive" } }
 ]
 }
 : {};

 if (filter.role) {
 where.role = filter.role;
 }

 const [items, total] = await this.prisma.$transaction([
 this.prisma.user.findMany({
 where,
 orderBy: { [filter.sortBy]: filter.sortOrder },
 ...toSkipTake(filter)
 }),
 this.prisma.user.count({ where })
 ]);

 return { items, total };
 }

 public update(id: string, data: UpdateUserBody & { passwordHash?: string }): Promise<User> {
 const updateData: Prisma.UserUpdateInput = {
 email: data.email,
 name: data.name,
 role: data.role,
 version: {
 increment: 1
 }
 };

 if (data.passwordHash) {
 updateData.passwordHash = data.passwordHash;
 }

 return this.prisma.user.update({
 where: {
 id,
 version: data.version
 },
 data: updateData
 });
 }

 public delete(id: string): Promise<User> {
 return this.prisma.user.delete({ where: { id } });
 }
}
```

```typescript
// FILE: apps/api/src/repositories/session.repository.ts
import type { PrismaClient, Session } from "@prisma/client";

export class SessionRepository {
 public constructor(private readonly prisma: PrismaClient) {}

 public create(data: {
 userId: string;
 refreshTokenHash: string;
 expiresAt: Date;
 ip?: string;
 userAgent?: string;
 }): Promise<Session> {
 return this.prisma.session.create({
 data
 });
 }

 public findById(id: string): Promise<Session | null> {
 return this.prisma.session.findUnique({ where: { id } });
 }

 public revokeById(id: string): Promise<Session> {
 return this.prisma.session.update({
 where: { id },
 data: {
 revokedAt: new Date()
 }
 });
 }

 public revokeAllByUser(userId: string): Promise<{ count: number }> {
 return this.prisma.session.updateMany({
 where: {
 userId,
 revokedAt: null
 },
 data: {
 revokedAt: new Date()
 }
 });
 }

 public deleteExpired(): Promise<{ count: number }> {
 return this.prisma.session.deleteMany({
 where: {
 expiresAt: {
 lte: new Date()
 }
 }
 });
 }
}
```

```typescript
// FILE: apps/api/src/repositories/project.repository.ts
import type { Prisma, PrismaClient, Project } from "@prisma/client";
import type { CreateProjectBody, ProjectFilter, UpdateProjectBody } from "@acme/shared";
import { toSkipTake } from "@acme/shared";

export class ProjectRepository {
 public constructor(private readonly prisma: PrismaClient) {}

 public create(data: CreateProjectBody): Promise<Project> {
 return this.prisma.project.create({ data });
 }

 public findById(id: string): Promise<Project | null> {
 return this.prisma.project.findUnique({ where: { id } });
 }

 public async findMany(filter: ProjectFilter): Promise<{ items: Project[]; total: number }> {
 const where: Prisma.ProjectWhereInput = {};

 if (filter.search) {
 where.OR = [
 { name: { contains: filter.search, mode: "insensitive" } },
 { description: { contains: filter.search, mode: "insensitive" } }
 ];
 }

 if (filter.ownerId) {
 where.ownerId = filter.ownerId;
 }

 const [items, total] = await this.prisma.$transaction([
 this.prisma.project.findMany({
 where,
 orderBy: { [filter.sortBy]: filter.sortOrder },
 ...toSkipTake(filter)
 }),
 this.prisma.project.count({ where })
 ]);

 return { items, total };
 }

 public update(id: string, data: UpdateProjectBody): Promise<Project> {
 return this.prisma.project.update({
 where: {
 id,
 version: data.version
 },
 data: {
 name: data.name,
 description: data.description,
 ownerId: data.ownerId,
 version: {
 increment: 1
 }
 }
 });
 }

 public delete(id: string): Promise<Project> {
 return this.prisma.project.delete({ where: { id } });
 }
}
```

```typescript
// FILE: apps/api/src/repositories/task.repository.ts
import type { Prisma, PrismaClient, Task } from "@prisma/client";
import type { CreateTaskBody, TaskFilter, TaskStatusTransition, UpdateTaskBody } from "@acme/shared";
import { toSkipTake } from "@acme/shared";

export class TaskRepository {
 public constructor(private readonly prisma: PrismaClient) {}

 public create(data: CreateTaskBody): Promise<Task> {
 return this.prisma.task.create({
 data: {
 ...data,
 dueDate: data.dueDate ? new Date(data.dueDate) : null
 }
 });
 }

 public findById(id: string): Promise<Task | null> {
 return this.prisma.task.findUnique({ where: { id } });
 }

 public async findMany(filter: TaskFilter): Promise<{ items: Task[]; total: number }> {
 const where: Prisma.TaskWhereInput = {};

 if (filter.projectId) {
 where.projectId = filter.projectId;
 }

 if (filter.assigneeId) {
 where.assigneeId = filter.assigneeId;
 }

 if (filter.status) {
 where.status = filter.status;
 }

 if (filter.search) {
 where.OR = [
 { title: { contains: filter.search, mode: "insensitive" } },
 { description: { contains: filter.search, mode: "insensitive" } }
 ];
 }

 const [items, total] = await this.prisma.$transaction([
 this.prisma.task.findMany({
 where,
 orderBy: { [filter.sortBy]: filter.sortOrder },
 ...toSkipTake(filter)
 }),
 this.prisma.task.count({ where })
 ]);

 return { items, total };
 }

 public update(id: string, data: UpdateTaskBody): Promise<Task> {
 return this.prisma.task.update({
 where: {
 id,
 version: data.version
 },
 data: {
 title: data.title,
 description: data.description,
 assigneeId: data.assigneeId,
 status: data.status,
 dueDate: data.dueDate !== undefined ? (data.dueDate ? new Date(data.dueDate) : null) : undefined,
 version: {
 increment: 1
 }
 }
 });
 }

 public transition(id: string, data: TaskStatusTransition): Promise<Task> {
 return this.prisma.task.update({
 where: {
 id,
 version: data.version
 },
 data: {
 status: data.status,
 version: {
 increment: 1
 }
 }
 });
 }

 public delete(id: string): Promise<Task> {
 return this.prisma.task.delete({ where: { id } });
 }
}
```

```typescript
// FILE: apps/api/src/services/audit.service.ts
import type { FastifyInstance, FastifyRequest } from "fastify";

export class AuditService {
 public constructor(private readonly fastify: FastifyInstance) {}

 public async log(request: FastifyRequest, input: {
 entityType: string;
 entityId?: string;
 action: "register" | "login" | "refresh" | "logout" | "create" | "update" | "delete" | "read" | "transition";
 metadata?: Record<string, unknown>;
 }): Promise<void> {
 await this.fastify.auditQueue.add("audit", {
 actorId: request.auth?.sub,
 actorEmail: request.auth?.email,
 entityType: input.entityType,
 entityId: input.entityId,
 action: input.action,
 metadata: {
 requestId: request.requestId,
 ...input.metadata
 },
 ip: request.ip
 });
 }
}
```

```typescript
// FILE: apps/api/src/services/auth.service.ts
import type { FastifyInstance, FastifyRequest } from "fastify";
import { ConflictError, NotFoundError, UnauthorizedError } from "@acme/shared";
import { parseDurationToMs } from "../utils/time.js";
import { hashPassword, verifyPassword } from "../auth/password.js";
import { signAccessToken, signRefreshToken, verifyRefreshToken } from "../auth/jwt.js";
import { UserRepository } from "../repositories/user.repository.js";
import { SessionRepository } from "../repositories/session.repository.js";

export class AuthService {
 private readonly userRepository: UserRepository;
 private readonly sessionRepository: SessionRepository;

 public constructor(private readonly fastify: FastifyInstance) {
 this.userRepository = new UserRepository(fastify.prisma);
 this.sessionRepository = new SessionRepository(fastify.prisma);
 }

 public async register(
 request: FastifyRequest,
 input: { email: string; password: string; name: string }
 ): Promise<{ user: Awaited<ReturnType<UserRepository["findById"]>> extends infer T ? NonNullable<T> : never; tokens: { accessToken: string; refreshToken: string } }> {
 const existing = await this.userRepository.findByEmail(input.email);
 if (existing) {
 throw new ConflictError("Email already registered");
 }

 const passwordHash = await hashPassword(input.password);
 const user = await this.userRepository.create({
 email: input.email,
 password: input.password,
 passwordHash,
 name: input.name,
 role: "viewer"
 });

 const session = await this.sessionRepository.create({
 userId: user.id,
 refreshTokenHash: "pending",
 expiresAt: new Date(Date.now() + parseDurationToMs(this.fastify.env.JWT_REFRESH_TTL)),
 ip: request.ip,
 userAgent: request.headers["user-agent"]
 });

 const accessToken = signAccessToken({
 sub: user.id,
 email: user.email,
 role: user.role,
 sessionId: session.id
 });

 const refreshToken = signRefreshToken({
 sub: user.id,
 email: user.email,
 role: user.role,
 sessionId: session.id
 });

 const refreshTokenHash = await hashPassword(refreshToken);

 await this.fastify.prisma.session.update({
 where: { id: session.id },
 data: { refreshTokenHash }
 });

 return {
 user,
 tokens: {
 accessToken,
 refreshToken
 }
 };
 }

 public async login(
 request: FastifyRequest,
 input: { email: string; password: string }
 ): Promise<{ user: Awaited<ReturnType<UserRepository["findById"]>> extends infer T ? NonNullable<T> : never; tokens: { accessToken: string; refreshToken: string } }> {
 const user = await this.userRepository.findByEmail(input.email);
 if (!user) {
 throw new UnauthorizedError("Invalid credentials");
 }

 const ok = await verifyPassword(user.passwordHash, input.password);
 if (!ok) {
 throw new UnauthorizedError("Invalid credentials");
 }

 const session = await this.sessionRepository.create({
 userId: user.id,
 refreshTokenHash: "pending",
 expiresAt: new Date(Date.now() + parseDurationToMs(this.fastify.env.JWT_REFRESH_TTL)),
 ip: request.ip,
 userAgent: request.headers["user-agent"]
 });

 const accessToken = signAccessToken({
 sub: user.id,
 email: user.email,
 role: user.role,
 sessionId: session.id
 });

 const refreshToken = signRefreshToken({
 sub: user.id,
 email: user.email,
 role: user.role,
 sessionId: session.id
 });

 const refreshTokenHash = await hashPassword(refreshToken);

 await this.fastify.prisma.session.update({
 where: { id: session.id },
 data: { refreshTokenHash }
 });

 return {
 user,
 tokens: {
 accessToken,
 refreshToken
 }
 };
 }

 public async refresh(
 request: FastifyRequest,
 input: { refreshToken: string }
 ): Promise<{ user: Awaited<ReturnType<UserRepository["findById"]>> extends infer T ? NonNullable<T> : never; tokens: { accessToken: string; refreshToken: string } }> {
 let claims;
 try {
 claims = verifyRefreshToken(input.refreshToken);
 } catch {
 throw new UnauthorizedError("Invalid refresh token");
 }

 const session = await this.sessionRepository.findById(claims.sessionId);
 if (!session || session.revokedAt || session.expiresAt <= new Date()) {
 throw new UnauthorizedError("Session expired");
 }

 const matches = await verifyPassword(session.refreshTokenHash, input.refreshToken);
 if (!matches) {
 await this.sessionRepository.revokeById(session.id);
 throw new UnauthorizedError("Refresh token reuse detected");
 }

 const user = await this.userRepository.findById(claims.sub);
 if (!user) {
 throw new NotFoundError("User not found");
 }

 await this.sessionRepository.revokeById(session.id);

 const nextSession = await this.sessionRepository.create({
 userId: user.id,
 refreshTokenHash: "pending",
 expiresAt: new Date(Date.now() + parseDurationToMs(this.fastify.env.JWT_REFRESH_TTL)),
 ip: request.ip,
 userAgent: request.headers["user-agent"]
 });

 const accessToken = signAccessToken({
 sub: user.id,
 email: user.email,
 role: user.role,
 sessionId: nextSession.id
 });

 const refreshToken = signRefreshToken({
 sub: user.id,
 email: user.email,
 role: user.role,
 sessionId: nextSession.id
 });

 const refreshTokenHash = await hashPassword(refreshToken);

 await this.fastify.prisma.session.update({
 where: { id: nextSession.id },
 data: {
 refreshTokenHash
 }
 });

 return {
 user,
 tokens: {
 accessToken,
 refreshToken
 }
 };
 }

 public async logout(input: { refreshToken: string }): Promise<void> {
 let claims;
 try {
 claims = verifyRefreshToken(input.refreshToken);
 } catch {
 throw new UnauthorizedError("Invalid refresh token");
 }

 const session = await this.sessionRepository.findById(claims.sessionId);
 if (!session) {
 return;
 }

 await this.sessionRepository.revokeById(session.id);
 }

 public async me(userId: string) {
 const user = await this.userRepository.findById(userId);
 if (!user) {
 throw new NotFoundError("User not found");
 }
 return user;
 }
}
```

```typescript
// FILE: apps/api/src/services/user.service.ts
import type { FastifyInstance, FastifyRequest } from "fastify";
import { ConflictError, NotFoundError, toPageResult } from "@acme/shared";
import type { CreateUserBody, UpdateUserBody, UserFilter } from "@acme/shared";
import { hashPassword } from "../auth/password.js";
import { UserRepository } from "../repositories/user.repository.js";
import { AuditService } from "./audit.service.js";

export class UserService {
 private readonly userRepository: UserRepository;
 private readonly auditService: AuditService;

 public constructor(private readonly fastify: FastifyInstance) {
 this.userRepository = new UserRepository(fastify.prisma);
 this.auditService = new AuditService(fastify);
 }

 public async create(request: FastifyRequest, input: CreateUserBody) {
 const existing = await this.userRepository.findByEmail(input.email);
 if (existing) {
 throw new ConflictError("Email already exists");
 }

 const passwordHash = await hashPassword(input.password);
 const user = await this.userRepository.create({ ...input, passwordHash });
 await this.auditService.log(request, {
 entityType: "user",
 entityId: user.id,
 action: "create",
 metadata: { email: user.email }
 });
 return user;
 }

 public async findById(request: FastifyRequest, id: string) {
 const user = await this.userRepository.findById(id);
 if (!user) {
 throw new NotFoundError("User not found");
 }
 await this.auditService.log(request, {
 entityType: "user",
 entityId: user.id,
 action: "read"
 });
 return user;
 }

 public async findMany(filter: UserFilter) {
 const { items, total } = await this.userRepository.findMany(filter);
 return toPageResult(items, total, filter);
 }

 public async update(request: FastifyRequest, id: string, input: UpdateUserBody) {
 const current = await this.userRepository.findById(id);
 if (!current) {
 throw new NotFoundError("User not found");
 }

 if (input.email && input.email !== current.email) {
 const existing = await this.userRepository.findByEmail(input.email);
 if (existing && existing.id !== id) {
 throw new ConflictError("Email already exists");
 }
 }

 const passwordHash = input.password ? await hashPassword(input.password) : undefined;
 const user = await this.userRepository.update(id, { ...input, passwordHash });
 await this.auditService.log(request, {
 entityType: "user",
 entityId: user.id,
 action: "update"
 });
 return user;
 }

 public async delete(request: FastifyRequest, id: string) {
 const existing = await this.userRepository.findById(id);
 if (!existing) {
 throw new NotFoundError("User not found");
 }
 const user = await this.userRepository.delete(id);
 await this.auditService.log(request, {
 entityType: "user",
 entityId: id,
 action: "delete"
 });
 return user;
 }
}
```

```typescript
// FILE: apps/api/src/services/project.service.ts
import type { FastifyInstance, FastifyRequest } from "fastify";
import { NotFoundError, toPageResult } from "@acme/shared";
import type { CreateProjectBody, ProjectFilter, UpdateProjectBody } from "@acme/shared";
import { ProjectRepository } from "../repositories/project.repository.js";
import { UserRepository } from "../repositories/user.repository.js";
import { AuditService } from "./audit.service.js";

export class ProjectService {
 private readonly projectRepository: ProjectRepository;
 private readonly userRepository: UserRepository;
 private readonly auditService: AuditService;

 public constructor(private readonly fastify: FastifyInstance) {
 this.projectRepository = new ProjectRepository(fastify.prisma);
 this.userRepository = new UserRepository(fastify.prisma);
 this.auditService = new AuditService(fastify);
 }

 public async create(request: FastifyRequest, input: CreateProjectBody) {
 const owner = await this.userRepository.findById(input.ownerId);
 if (!owner) {
 throw new NotFoundError("Owner not found");
 }
 const project = await this.projectRepository.create(input);
 await this.auditService.log(request, {
 entityType: "project",
 entityId: project.id,
 action: "create"
 });
 return project;
 }

 public async findById(request: FastifyRequest, id: string) {
 const project = await this.projectRepository.findById(id);
 if (!project) {
 throw new NotFoundError("Project not found");
 }
 await this.auditService.log(request, {
 entityType: "project",
 entityId: id,
 action: "read"
 });
 return project;
 }

 public async findMany(filter: ProjectFilter) {
 const { items, total } = await this.projectRepository.findMany(filter);
 return toPageResult(items, total, filter);
 }

 public async update(request: FastifyRequest, id: string, input: UpdateProjectBody) {
 const existing = await this.projectRepository.findById(id);
 if (!existing) {
 throw new NotFoundError("Project not found");
 }
 if (input.ownerId) {
 const owner = await this.userRepository.findById(input.ownerId);
 if (!owner) {
 throw new NotFoundError("Owner not found");
 }
 }
 const project = await this.projectRepository.update(id, input);
 await this.auditService.log(request, {
 entityType: "project",
 entityId: id,
 action: "update"
 });
 return project;
 }

 public async delete(request: FastifyRequest, id: string) {
 const existing = await this.projectRepository.findById(id);
 if (!existing) {
 throw new NotFoundError("Project not found");
 }
 const project = await this.projectRepository.delete(id);
 await this.auditService.log(request, {
 entityType: "project",
 entityId: id,
 action: "delete"
 });
 return project;
 }
}
```

```typescript
// FILE: apps/api/src/services/task.service.ts
import type { FastifyInstance, FastifyRequest } from "fastify";
import { ConflictError, NotFoundError, toPageResult } from "@acme/shared";
import type { CreateTaskBody, TaskFilter, TaskStatusTransition, UpdateTaskBody } from "@acme/shared";
import { TaskRepository } from "../repositories/task.repository.js";
import { ProjectRepository } from "../repositories/project.repository.js";
import { UserRepository } from "../repositories/user.repository.js";
import { AuditService } from "./audit.service.js";

const transitions: Record<string, string[]> = {
 todo: ["in_progress", "blocked", "done"],
 in_progress: ["blocked", "done"],
 blocked: ["in_progress", "done"],
 done: []
};

export class TaskService {
 private readonly taskRepository: TaskRepository;
 private readonly projectRepository: ProjectRepository;
 private readonly userRepository: UserRepository;
 private readonly auditService: AuditService;

 public constructor(private readonly fastify: FastifyInstance) {
 this.taskRepository = new TaskRepository(fastify.prisma);
 this.projectRepository = new ProjectRepository(fastify.prisma);
 this.userRepository = new UserRepository(fastify.prisma);
 this.auditService = new AuditService(fastify);
 }

 public async create(request: FastifyRequest, input: CreateTaskBody) {
 const project = await this.projectRepository.findById(input.projectId);
 if (!project) {
 throw new NotFoundError("Project not found");
 }
 if (input.assigneeId) {
 const assignee = await this.userRepository.findById(input.assigneeId);
 if (!assignee) {
 throw new NotFoundError("Assignee not found");
 }
 }
 const task = await this.taskRepository.create(input);
 await this.fastify.realtimeQueue.add("task.created", {
 type: "task.created",
 data: {
 id: task.id,
 projectId: task.projectId,
 title: task.title,
 status: task.status,
 version: task.version
 }
 });
 await this.auditService.log(request, {
 entityType: "task",
 entityId: task.id,
 action: "create"
 });
 return task;
 }

 public async findById(request: FastifyRequest, id: string) {
 const task = await this.taskRepository.findById(id);
 if (!task) {
 throw new NotFoundError("Task not found");
 }
 await this.auditService.log(request, {
 entityType: "task",
 entityId: id,
 action: "read"
 });
 return task;
 }

 public async findMany(filter: TaskFilter) {
 const { items, total } = await this.taskRepository.findMany(filter);
 return toPageResult(items, total, filter);
 }

 public async update(request: FastifyRequest, id: string, input: UpdateTaskBody) {
 const existing = await this.taskRepository.findById(id);
 if (!existing) {
 throw new NotFoundError("Task not found");
 }

 if (input.assigneeId) {
 const assignee = await this.userRepository.findById(input.assigneeId);
 if (!assignee) {
 throw new NotFoundError("Assignee not found");
 }
 }

 if (input.status && !transitions[existing.status].includes(input.status) && existing.status !== input.status) {
 throw new ConflictError(`Invalid task status transition from ${existing.status} to ${input.status}`);
 }

 const task = await this.taskRepository.update(id, input);
 await this.fastify.realtimeQueue.add("task.updated", {
 type: "task.updated",
 data: {
 id: task.id,
 projectId: task.projectId,
 title: task.title,
 status: task.status,
 version: task.version
 }
 });
 await this.auditService.log(request, {
 entityType: "task",
 entityId: id,
 action: "update"
 });
 return task;
 }

 public async transition(request: FastifyRequest, id: string, input: TaskStatusTransition) {
 const existing = await this.taskRepository.findById(id);
 if (!existing) {
 throw new NotFoundError("Task not found");
 }
 if (!transitions[existing.status].includes(input.status) && existing.status !== input.status) {
 throw new ConflictError(`Invalid task status transition from ${existing.status} to ${input.status}`);
 }
 const task = await this.taskRepository.transition(id, input);
 await this.fastify.realtimeQueue.add("task.updated", {
 type: "task.updated",
 data: {
 id: task.id,
 projectId: task.projectId,
 title: task.title,
 status: task.status,
 version: task.version
 }
 });
 await this.auditService.log(request, {
 entityType: "task",
 entityId: id,
 action: "transition"
 });
 return task;
 }

 public async delete(request: FastifyRequest, id: string) {
 const existing = await this.taskRepository.findById(id);
 if (!existing) {
 throw new NotFoundError("Task not found");
 }
 const task = await this.taskRepository.delete(id);
 await this.fastify.realtimeQueue.add("task.deleted", {
 type: "task.deleted",
 data: {
 id: task.id,
 projectId: task.projectId
 }
 });
 await this.auditService.log(request, {
 entityType: "task",
 entityId: id,
 action: "delete"
 });
 return task;
 }
}
```

```typescript
// FILE: apps/api/src/controllers/auth.controller.ts
import type { FastifyReply, FastifyRequest } from "fastify";
import type { AuthService } from "../services/auth.service.js";

function serializeUser(user: {
 id: string;
 email: string;
 name: string;
 role: string;
 version: number;
 createdAt: Date;
 updatedAt: Date;
}) {
 return {
 id: user.id,
 email: user.email,
 name: user.name,
 role: user.role,
 version: user.version,
 createdAt: user.createdAt.toISOString(),
 updatedAt: user.updatedAt.toISOString()
 };
}

export class AuthController {
 public constructor(private readonly authService: AuthService) {}

 public register = async (request: FastifyRequest, reply: FastifyReply) => {
 const result = await this.authService.register(request, request.body as { email: string; password: string; name: string });
 return reply.status(201).send({
 user: serializeUser(result.user),
 tokens: result.tokens
 });
 };

 public login = async (request: FastifyRequest, reply: FastifyReply) => {
 const result = await this.authService.login(request, request.body as { email: string; password: string });
 return reply.send({
 user: serializeUser(result.user),
 tokens: result.tokens
 });
 };

 public refresh = async (request: FastifyRequest, reply: FastifyReply) => {
 const result = await this.authService.refresh(request, request.body as { refreshToken: string });
 return reply.send({
 user: serializeUser(result.user),
 tokens: result.tokens
 });
 };

 public logout = async (request: FastifyRequest, reply: FastifyReply) => {
 await this.authService.logout(request.body as { refreshToken: string });
 return reply.status(204).send();
 };

 public me = async (request: FastifyRequest, reply: FastifyReply) => {
 const user = await this.authService.me(request.auth!.sub);
 return reply.send(serializeUser(user));
 };
}
```

```typescript
// FILE: apps/api/src/controllers/user.controller.ts
import type { FastifyReply, FastifyRequest } from "fastify";
import type { UserService } from "../services/user.service.js";

function serializeUser(user: {
 id: string;
 email: string;
 name: string;
 role: string;
 version: number;
 createdAt: Date;
 updatedAt: Date;
}) {
 return {
 id: user.id,
 email: user.email,
 name: user.name,
 role: user.role,
 version: user.version,
 createdAt: user.createdAt.toISOString(),
 updatedAt: user.updatedAt.toISOString()
 };
}

export class UserController {
 public constructor(private readonly userService: UserService) {}

 public create = async (request: FastifyRequest, reply: FastifyReply) => {
 const user = await this.userService.create(request, request.body as never);
 return reply.status(201).send(serializeUser(user));
 };

 public getById = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const user = await this.userService.findById(request, params.id);
 return reply.send(serializeUser(user));
 };

 public list = async (request: FastifyRequest, reply: FastifyReply) => {
 const page = await this.userService.findMany(request.query as never);
 return reply.send({
 ...page,
 items: page.items.map(serializeUser)
 });
 };

 public update = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const user = await this.userService.update(request, params.id, request.body as never);
 return reply.send(serializeUser(user));
 };

 public delete = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const user = await this.userService.delete(request, params.id);
 return reply.send(serializeUser(user));
 };
}
```

```typescript
// FILE: apps/api/src/controllers/project.controller.ts
import type { FastifyReply, FastifyRequest } from "fastify";
import type { ProjectService } from "../services/project.service.js";

function serializeProject(project: {
 id: string;
 name: string;
 description: string | null;
 ownerId: string;
 version: number;
 createdAt: Date;
 updatedAt: Date;
}) {
 return {
 id: project.id,
 name: project.name,
 description: project.description,
 ownerId: project.ownerId,
 version: project.version,
 createdAt: project.createdAt.toISOString(),
 updatedAt: project.updatedAt.toISOString()
 };
}

export class ProjectController {
 public constructor(private readonly projectService: ProjectService) {}

 public create = async (request: FastifyRequest, reply: FastifyReply) => {
 const project = await this.projectService.create(request, request.body as never);
 return reply.status(201).send(serializeProject(project));
 };

 public getById = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const project = await this.projectService.findById(request, params.id);
 return reply.send(serializeProject(project));
 };

 public list = async (request: FastifyRequest, reply: FastifyReply) => {
 const page = await this.projectService.findMany(request.query as never);
 return reply.send({
 ...page,
 items: page.items.map(serializeProject)
 });
 };

 public update = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const project = await this.projectService.update(request, params.id, request.body as never);
 return reply.send(serializeProject(project));
 };

 public delete = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const project = await this.projectService.delete(request, params.id);
 return reply.send(serializeProject(project));
 };
}
```

```typescript
// FILE: apps/api/src/controllers/task.controller.ts
import type { FastifyReply, FastifyRequest } from "fastify";
import type { TaskService } from "../services/task.service.js";

function serializeTask(task: {
 id: string;
 projectId: string;
 title: string;
 description: string | null;
 assigneeId: string | null;
 status: string;
 version: number;
 dueDate: Date | null;
 createdAt: Date;
 updatedAt: Date;
}) {
 return {
 id: task.id,
 projectId: task.projectId,
 title: task.title,
 description: task.description,
 assigneeId: task.assigneeId,
 status: task.status,
 version: task.version,
 dueDate: task.dueDate?.toISOString() ?? null,
 createdAt: task.createdAt.toISOString(),
 updatedAt: task.updatedAt.toISOString()
 };
}

export class TaskController {
 public constructor(private readonly taskService: TaskService) {}

 public create = async (request: FastifyRequest, reply: FastifyReply) => {
 const task = await this.taskService.create(request, request.body as never);
 return reply.status(201).send(serializeTask(task));
 };

 public getById = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const task = await this.taskService.findById(request, params.id);
 return reply.send(serializeTask(task));
 };

 public list = async (request: FastifyRequest, reply: FastifyReply) => {
 const page = await this.taskService.findMany(request.query as never);
 return reply.send({
 ...page,
 items: page.items.map(serializeTask)
 });
 };

 public update = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const task = await this.taskService.update(request, params.id, request.body as never);
 return reply.send(serializeTask(task));
 };

 public transition = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const task = await this.taskService.transition(request, params.id, request.body as never);
 return reply.send(serializeTask(task));
 };

 public delete = async (request: FastifyRequest, reply: FastifyReply) => {
 const params = request.params as { id: string };
 const task = await this.taskService.delete(request, params.id);
 return reply.send(serializeTask(task));
 };
}
```

```typescript
// FILE: apps/api/src/routes/health.routes.ts
import type { FastifyPluginAsync } from "fastify";

const healthRoutes: FastifyPluginAsync = async (fastify) => {
 fastify.get("/health", async () => {
 return {
 status: "ok",
 uptime: process.uptime()
 };
 });

 fastify.get("/ready", async () => {
 await fastify.prisma.$queryRaw`SELECT 1`;
 await fastify.redis.ping();
 return {
 status: "ready"
 };
 });
};

export default healthRoutes;
```

```typescript
// FILE: apps/api/src/routes/auth.routes.ts
import type { FastifyPluginAsync } from "fastify";
import {
 authResponseSchema,
 loginBodySchema,
 logoutBodySchema,
 refreshBodySchema,
 registerBodySchema,
 userResponseSchema
} from "@acme/shared";
import { authenticate } from "../middleware/authenticate.js";
import { AuthService } from "../services/auth.service.js";
import { AuthController } from "../controllers/auth.controller.js";

const authRoutes: FastifyPluginAsync = async (fastify) => {
 const controller = new AuthController(new AuthService(fastify));

 fastify.post(
 "/auth/register",
 {
 schema: {
 tags: ["auth"],
 body: registerBodySchema,
 response: {
 201: authResponseSchema
 }
 }
 },
 controller.register
 );

 fastify.post(
 "/auth/login",
 {
 schema: {
 tags: ["auth"],
 body: loginBodySchema,
 response: {
 200: authResponseSchema
 }
 }
 },
 controller.login
 );

 fastify.post(
 "/auth/refresh",
 {
 schema: {
 tags: ["auth"],
 body: refreshBodySchema,
 response: {
 200: authResponseSchema
 }
 }
 },
 controller.refresh
 );

 fastify.post(
 "/auth/logout",
 {
 schema: {
 tags: ["auth"],
 body: logoutBodySchema
 }
 },
 controller.logout
 );

 fastify.get(
 "/auth/me",
 {
 schema: {
 tags: ["auth"],
 security: [{ bearerAuth: [] }],
 response: {
 200: userResponseSchema
 }
 },
 preHandler: [authenticate]
 },
 controller.me
 );
};

export default authRoutes;
```

```typescript
// FILE: apps/api/src/routes/user.routes.ts
import type { FastifyPluginAsync } from "fastify";
import {
 createUserBodySchema,
 idParamSchema,
 pagedUsersResponseSchema,
 updateUserBodySchema,
 userFilterSchema,
 userResponseSchema
} from "@acme/shared";
import { authenticate } from "../middleware/authenticate.js";
import { authorize } from "../middleware/authorize.js";
import { UserService } from "../services/user.service.js";
import { UserController } from "../controllers/user.controller.js";

const userRoutes: FastifyPluginAsync = async (fastify) => {
 const controller = new UserController(new UserService(fastify));

 fastify.post(
 "/users",
 {
 schema: {
 tags: ["users"],
 security: [{ bearerAuth: [] }],
 body: createUserBodySchema,
 response: { 201: userResponseSchema }
 },
 preHandler: [authenticate, authorize("admin")]
 },
 controller.create
 );

 fastify.get(
 "/users",
 {
 schema: {
 tags: ["users"],
 security: [{ bearerAuth: [] }],
 querystring: userFilterSchema,
 response: { 200: pagedUsersResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.list
 );

 fastify.get(
 "/users/:id",
 {
 schema: {
 tags: ["users"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 response: { 200: userResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.getById
 );

 fastify.put(
 "/users/:id",
 {
 schema: {
 tags: ["users"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 body: updateUserBodySchema,
 response: { 200: userResponseSchema }
 },
 preHandler: [authenticate, authorize("admin")]
 },
 controller.update
 );

 fastify.delete(
 "/users/:id",
 {
 schema: {
 tags: ["users"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 response: { 200: userResponseSchema }
 },
 preHandler: [authenticate, authorize("admin")]
 },
 controller.delete
 );
};

export default userRoutes;
```

```typescript
// FILE: apps/api/src/routes/project.routes.ts
import type { FastifyPluginAsync } from "fastify";
import {
 createProjectBodySchema,
 idParamSchema,
 pagedProjectsResponseSchema,
 projectFilterSchema,
 projectResponseSchema,
 updateProjectBodySchema
} from "@acme/shared";
import { authenticate } from "../middleware/authenticate.js";
import { authorize } from "../middleware/authorize.js";
import { ProjectService } from "../services/project.service.js";
import { ProjectController } from "../controllers/project.controller.js";

const projectRoutes: FastifyPluginAsync = async (fastify) => {
 const controller = new ProjectController(new ProjectService(fastify));

 fastify.post(
 "/projects",
 {
 schema: {
 tags: ["projects"],
 security: [{ bearerAuth: [] }],
 body: createProjectBodySchema,
 response: { 201: projectResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.create
 );

 fastify.get(
 "/projects",
 {
 schema: {
 tags: ["projects"],
 security: [{ bearerAuth: [] }],
 querystring: projectFilterSchema,
 response: { 200: pagedProjectsResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor", "viewer")]
 },
 controller.list
 );

 fastify.get(
 "/projects/:id",
 {
 schema: {
 tags: ["projects"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 response: { 200: projectResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor", "viewer")]
 },
 controller.getById
 );

 fastify.put(
 "/projects/:id",
 {
 schema: {
 tags: ["projects"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 body: updateProjectBodySchema,
 response: { 200: projectResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.update
 );

 fastify.delete(
 "/projects/:id",
 {
 schema: {
 tags: ["projects"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 response: { 200: projectResponseSchema }
 },
 preHandler: [authenticate, authorize("admin")]
 },
 controller.delete
 );
};

export default projectRoutes;
```

```typescript
// FILE: apps/api/src/routes/task.routes.ts
import type { FastifyPluginAsync } from "fastify";
import {
 createTaskBodySchema,
 idParamSchema,
 pagedTasksResponseSchema,
 taskFilterSchema,
 taskResponseSchema,
 taskStatusTransitionSchema,
 updateTaskBodySchema
} from "@acme/shared";
import { authenticate } from "../middleware/authenticate.js";
import { authorize } from "../middleware/authorize.js";
import { TaskService } from "../services/task.service.js";
import { TaskController } from "../controllers/task.controller.js";

const taskRoutes: FastifyPluginAsync = async (fastify) => {
 const controller = new TaskController(new TaskService(fastify));

 fastify.post(
 "/tasks",
 {
 schema: {
 tags: ["tasks"],
 security: [{ bearerAuth: [] }],
 body: createTaskBodySchema,
 response: { 201: taskResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.create
 );

 fastify.get(
 "/tasks",
 {
 schema: {
 tags: ["tasks"],
 security: [{ bearerAuth: [] }],
 querystring: taskFilterSchema,
 response: { 200: pagedTasksResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor", "viewer")]
 },
 controller.list
 );

 fastify.get(
 "/tasks/:id",
 {
 schema: {
 tags: ["tasks"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 response: { 200: taskResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor", "viewer")]
 },
 controller.getById
 );

 fastify.put(
 "/tasks/:id",
 {
 schema: {
 tags: ["tasks"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 body: updateTaskBodySchema,
 response: { 200: taskResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.update
 );

 fastify.post(
 "/tasks/:id/transition",
 {
 schema: {
 tags: ["tasks"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 body: taskStatusTransitionSchema,
 response: { 200: taskResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.transition
 );

 fastify.delete(
 "/tasks/:id",
 {
 schema: {
 tags: ["tasks"],
 security: [{ bearerAuth: [] }],
 params: idParamSchema,
 response: { 200: taskResponseSchema }
 },
 preHandler: [authenticate, authorize("admin", "editor")]
 },
 controller.delete
 );
};

export default taskRoutes;
```

```typescript
// FILE: apps/api/src/app.ts
import Fastify from "fastify";
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from "fastify-type-provider-zod";
import { env } from "./config/env.js";
import { logger } from "./lib/logger.js";
import { errorHandler } from "./lib/errors.js";
import prismaPlugin from "./plugins/prisma.js";
import redisPlugin from "./plugins/redis.js";
import securityPlugin from "./plugins/security.js";
import requestContextPlugin from "./plugins/request-context.js";
import metricsPlugin from "./lib/metrics.js";
import swaggerPlugin from "./plugins/swagger.js";
import realtimePlugin from "./plugins/realtime.js";
import rateLimitPlugin from "./plugins/rate-limit.js";
import healthRoutes from "./routes/health.routes.js";
import authRoutes from "./routes/auth.routes.js";
import userRoutes from "./routes/user.routes.js";
import projectRoutes from "./routes/project.routes.js";
import taskRoutes from "./routes/task.routes.js";

export async function buildApp() {
 const app = Fastify({
 logger,
 requestTimeout: env.REQUEST_TIMEOUT_MS
 }).withTypeProvider<ZodTypeProvider>();

 app.decorate("env", env);
 app.setValidatorCompiler(validatorCompiler);
 app.setSerializerCompiler(serializerCompiler);
 app.setErrorHandler(errorHandler);

 await app.register(requestContextPlugin);
 await app.register(prismaPlugin);
 await app.register(securityPlugin);
 await app.register(metricsPlugin);
 await app.register(realtimePlugin);
 await app.register(redisPlugin);
 await app.register(swaggerPlugin);

 app.addHook("preHandler", async (request) => {
 const authorization = request.headers.authorization;
 if (authorization?.startsWith("Bearer ")) {
 try {
 const { verifyAccessToken } = await import("./auth/jwt.js");
 request.auth = verifyAccessToken(authorization.slice(7));
 } catch {
 }
 }
 });

 await app.register(rateLimitPlugin);
 await app.register(healthRoutes);
 await app.register(authRoutes, { prefix: "/api/v1" });
 await app.register(userRoutes, { prefix: "/api/v1" });
 await app.register(projectRoutes, { prefix: "/api/v1" });
 await app.register(taskRoutes, { prefix: "/api/v1" });

 return app;
}
```

```typescript
// FILE: apps/api/src/server.ts
import { buildApp } from "./app.js";
import { env } from "./config/env.js";

async function main(): Promise<void> {
 const app = await buildApp();
 try {
 await app.listen({
 host: env.HOST,
 port: env.PORT
 });
 app.log.info(`server listening on ${env.HOST}:${env.PORT}`);
 } catch (error) {
 app.log.error(error);
 process.exit(1);
 }
}

void main();
```

```typescript
// FILE: apps/api/tests/helpers/fakes.ts
import { vi } from "vitest";

export function createFakeRequest(overrides?: Record<string, unknown>) {
 return {
 ip: "127.0.0.1",
 requestId: "req-1",
 headers: {},
 auth: {
 sub: "user-1",
 email: "user@example.com",
 role: "admin",
 sessionId: "session-1",
 type: "access"
 },
 server: {
 metrics: {
 authFailureCounter: {
 labels: vi.fn().mockReturnValue({ inc: vi.fn() })
 }
 }
 },
 ...overrides
 };
}

export function createFakeReply() {
 return {
 code: 200,
 headers: {} as Record<string, string>,
 status(code: number) {
 this.code = code;
 return this;
 },
 header(key: string, value: string) {
 this.headers[key] = value;
 return this;
 },
 send: vi.fn()
 };
}
```

```typescript
// FILE: apps/api/tests/unit/shared.contracts.test.ts
import { describe, expect, it } from "vitest";
import { createTaskBodySchema, loginBodySchema, registerBodySchema } from "@acme/shared";

describe("shared contracts", () => {
 it("accepts valid registration payload", () => {
 const payload = registerBodySchema.parse({
 email: "a@example.com",
 password: "Password123!",
 name: "Alice Doe"
 });
 expect(payload.email).toBe("a@example.com");
 });

 it("rejects invalid login payload", () => {
 expect(() =>
 loginBodySchema.parse({
 email: "invalid",
 password: "123"
 })
 ).toThrow();
 });

 it("accepts task body with nullable due date", () => {
 const payload = createTaskBodySchema.parse({
 projectId: "7cb01622-7fa0-4f0c-b512-63bdb11b5351",
 title: "Task A",
 dueDate: null
 });
 expect(payload.dueDate).toBeNull();
 });
});
```

```typescript
// FILE: apps/api/tests/unit/password.test.ts
import { describe, expect, it } from "vitest";
import { hashPassword, verifyPassword } from "../../src/auth/password.js";

describe("password helpers", () => {
 it("hashes and verifies passwords", async () => {
 const hash = await hashPassword("Password123!");
 expect(hash).not.toBe("Password123!");
 await expect(verifyPassword(hash, "Password123!")).resolves.toBe(true);
 });

 it("fails invalid password", async () => {
 const hash = await hashPassword("Password123!");
 await expect(verifyPassword(hash, "Password123?")).resolves.toBe(false);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/jwt.test.ts
import { describe, expect, it } from "vitest";
import { signAccessToken, signRefreshToken, verifyAccessToken, verifyRefreshToken } from "../../src/auth/jwt.js";

describe("jwt helpers", () => {
 const claims = {
 sub: "user-1",
 email: "user@example.com",
 role: "admin" as const,
 sessionId: "session-1"
 };

 it("signs and verifies access token", () => {
 const token = signAccessToken(claims);
 const decoded = verifyAccessToken(token);
 expect(decoded.sub).toBe(claims.sub);
 expect(decoded.type).toBe("access");
 });

 it("signs and verifies refresh token", () => {
 const token = signRefreshToken(claims);
 const decoded = verifyRefreshToken(token);
 expect(decoded.type).toBe("refresh");
 expect(decoded.sessionId).toBe(claims.sessionId);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/time.test.ts
import { describe, expect, it } from "vitest";
import { addMs, parseDurationToMs } from "../../src/utils/time.js";

describe("time utilities", () => {
 it("parses minutes", () => {
 expect(parseDurationToMs("15m")).toBe(900000);
 });

 it("adds milliseconds", () => {
 const start = new Date("2026-03-07T00:00:00.000Z");
 expect(addMs(start, 1000).toISOString()).toBe("2026-03-07T00:00:01.000Z");
 });
});
```

```typescript
// FILE: apps/api/tests/unit/ids.test.ts
import { describe, expect, it } from "vitest";
import { createRequestId } from "../../src/utils/ids.js";

describe("ids", () => {
 it("creates unique request ids", () => {
 const a = createRequestId();
 const b = createRequestId();
 expect(a).not.toBe(b);
 expect(a).toMatch(
 /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
 );
 });
});
```

```typescript
// FILE: apps/api/tests/unit/authorize.test.ts
import { describe, expect, it } from "vitest";
import { authorize } from "../../src/middleware/authorize.js";
import { createFakeReply, createFakeRequest } from "../helpers/fakes.js";

describe("authorize middleware", () => {
 it("allows matching roles", async () => {
 const guard = authorize("admin");
 await expect(guard(createFakeRequest(), createFakeReply() as never)).resolves.toBeUndefined();
 });

 it("rejects non-matching roles", async () => {
 const guard = authorize("viewer");
 await expect(
 guard(createFakeRequest({ auth: { role: "editor" } }), createFakeReply() as never)
 ).rejects.toThrow("Forbidden");
 });
});
```

```typescript
// FILE: apps/api/tests/unit/authenticate.test.ts
import { describe, expect, it } from "vitest";
import { authenticate } from "../../src/middleware/authenticate.js";
import { signAccessToken } from "../../src/auth/jwt.js";
import { createFakeReply, createFakeRequest } from "../helpers/fakes.js";

describe("authenticate middleware", () => {
 it("accepts valid bearer token", async () => {
 const token = signAccessToken({
 sub: "user-1",
 email: "user@example.com",
 role: "admin",
 sessionId: "session-1"
 });
 const request = createFakeRequest({
 headers: {
 authorization: `Bearer ${token}`
 }
 });
 await expect(authenticate(request as never, createFakeReply() as never)).resolves.toBeUndefined();
 });

 it("rejects missing token", async () => {
 await expect(authenticate(createFakeRequest() as never, createFakeReply() as never)).rejects.toThrow(
 "Missing bearer token"
 );
 });
});
```

```typescript
// FILE: apps/api/tests/unit/realtime-hub.test.ts
import { describe, expect, it, vi } from "vitest";
import { RealtimeHub } from "../../src/realtime/hub.js";

describe("realtime hub", () => {
 it("tracks clients and broadcasts", () => {
 const socket = {
 readyState: 1,
 send: vi.fn(),
 on: vi.fn()
 };

 const hub = new RealtimeHub();
 hub.addClient({
 id: "c1",
 socket: socket as never,
 request: {} as never
 });

 hub.broadcast({
 type: "task.updated",
 payload: { id: "t1" }
 });

 expect(hub.size()).toBe(1);
 expect(socket.send).toHaveBeenCalledOnce();
 });
});
```

```typescript
// FILE: apps/api/tests/unit/error-handler.test.ts
import { describe, expect, it, vi } from "vitest";
import { AppError } from "@acme/shared";
import { errorHandler } from "../../src/lib/errors.js";

describe("error handler", () => {
 it("formats app error", () => {
 const request = {
 requestId: "req-1",
 log: { error: vi.fn() }
 };
 const reply = {
 status: vi.fn().mockReturnThis(),
 send: vi.fn()
 };
 errorHandler(new AppError(400, "BAD", "Bad request"), request as never, reply as never);
 expect(reply.status).toHaveBeenCalledWith(400);
 expect(reply.send).toHaveBeenCalled();
 });
});
```

```typescript
// FILE: apps/api/tests/unit/request-context.test.ts
import { describe, expect, it } from "vitest";
import requestContextPlugin from "../../src/plugins/request-context.js";
import Fastify from "fastify";

describe("request context plugin", () => {
 it("sets request id header", async () => {
 const app = Fastify();
 await app.register(requestContextPlugin);
 app.get("/", async (request, reply) => {
 reply.send({ requestId: request.requestId });
 });
 const res = await app.inject({ method: "GET", url: "/" });
 expect(res.headers["x-request-id"]).toBeDefined();
 });
});
```

```typescript
// FILE: apps/api/tests/unit/security-sanitize.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import securityPlugin from "../../src/plugins/security.js";

describe("security plugin sanitize", () => {
 it("sanitizes body strings", async () => {
 const app = Fastify();
 app.decorate("env", {
 CORS_ORIGIN: "http://localhost:3000"
 } as never);
 await app.register(securityPlugin);
 app.post("/", async (request) => request.body);
 const res = await app.inject({
 method: "POST",
 url: "/",
 payload: {
 value: "<b>hello</b>"
 }
 });
 expect(res.json().value).toBe("bhello/b");
 });
});
```

```typescript
// FILE: apps/api/tests/unit/rate-limit-key.test.ts
import { describe, expect, it, vi } from "vitest";
import rateLimitPlugin from "../../src/plugins/rate-limit.js";
import Fastify from "fastify";

describe("rate limit plugin", () => {
 it("allows requests under threshold", async () => {
 const app = Fastify();
 const redis = {
 incr: vi.fn().mockResolvedValue(1),
 expire: vi.fn().mockResolvedValue(1)
 };
 app.decorate("redis", redis as never);
 app.decorate("env", {
 RATE_LIMIT_IP_MAX: 2,
 RATE_LIMIT_USER_MAX: 2,
 RATE_LIMIT_WINDOW_SEC: 60
 } as never);
 await app.register(rateLimitPlugin);
 app.get("/", async () => ({ ok: true }));
 const res = await app.inject({ method: "GET", url: "/" });
 expect(res.statusCode).toBe(200);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/user-service-logic.test.ts
import { describe, expect, it, vi } from "vitest";
import { UserService } from "../../src/services/user.service.js";

describe("user service construction", () => {
 it("can construct service with dependencies", () => {
 const fastify = {
 prisma: {},
 auditQueue: {},
 realtimeQueue: {}
 };
 const service = new UserService(fastify as never);
 expect(service).toBeInstanceOf(UserService);
 });

 it("exposes findMany method", () => {
 const fastify = {
 prisma: {},
 auditQueue: {},
 realtimeQueue: {}
 };
 const service = new UserService(fastify as never);
 expect(typeof service.findMany).toBe("function");
 expect(vi.isMockFunction((service as never).findMany)).toBe(false);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/project-service-logic.test.ts
import { describe, expect, it } from "vitest";
import { ProjectService } from "../../src/services/project.service.js";

describe("project service construction", () => {
 it("constructs service", () => {
 const fastify = {
 prisma: {},
 auditQueue: {},
 realtimeQueue: {}
 };
 const service = new ProjectService(fastify as never);
 expect(service).toBeInstanceOf(ProjectService);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/task-service-transition-map.test.ts
import { describe, expect, it } from "vitest";
import { TaskService } from "../../src/services/task.service.js";

describe("task service construction", () => {
 it("constructs service", () => {
 const fastify = {
 prisma: {},
 auditQueue: {},
 realtimeQueue: {}
 };
 const service = new TaskService(fastify as never);
 expect(service).toBeInstanceOf(TaskService);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/metrics-plugin.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import metricsPlugin from "../../src/lib/metrics.js";

describe("metrics plugin", () => {
 it("exposes metrics endpoint", async () => {
 const app = Fastify();
 await app.register(metricsPlugin);
 const res = await app.inject({ method: "GET", url: "/metrics" });
 expect(res.statusCode).toBe(200);
 expect(res.headers["content-type"]).toContain("text/plain");
 });
});
```

```typescript
// FILE: apps/api/tests/unit/swagger-plugin.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import swaggerPlugin from "../../src/plugins/swagger.js";

describe("swagger plugin", () => {
 it("registers docs route when enabled", async () => {
 const app = Fastify();
 app.decorate("env", {
 SWAGGER_ENABLED: true
 } as never);
 await app.register(swaggerPlugin);
 app.get("/", async () => ({ ok: true }));
 await app.ready();
 const res = await app.inject({ method: "GET", url: "/docs" });
 expect([200, 302]).toContain(res.statusCode);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/contracts-pagination.test.ts
import { describe, expect, it } from "vitest";
import { pageQuerySchema, toPageResult, toSkipTake } from "@acme/shared";

describe("pagination utilities", () => {
 it("computes skip/take", () => {
 const query = pageQuerySchema.parse({ page: 2, pageSize: 10 });
 expect(toSkipTake(query)).toEqual({ skip: 10, take: 10 });
 });

 it("computes page result", () => {
 const query = pageQuerySchema.parse({ page: 1, pageSize: 2 });
 const result = toPageResult([1, 2], 5, query);
 expect(result.pageCount).toBe(3);
 });
});
```

```typescript
// FILE: apps/api/tests/unit/auth-controller.test.ts
import { describe, expect, it, vi } from "vitest";
import { AuthController } from "../../src/controllers/auth.controller.js";
import { createFakeReply, createFakeRequest } from "../helpers/fakes.js";

describe("auth controller", () => {
 it("returns me payload", async () => {
 const controller = new AuthController({
 me: vi.fn().mockResolvedValue({
 id: "u1",
 email: "a@example.com",
 name: "Alice",
 role: "admin",
 version: 1,
 createdAt: new Date("2026-03-07T00:00:00.000Z"),
 updatedAt: new Date("2026-03-07T00:00:00.000Z")
 })
 } as never);

 const reply = createFakeReply();
 await controller.me(createFakeRequest() as never, reply as never);
 expect(reply.send).toHaveBeenCalled();
 });
});
```

```typescript
// FILE: apps/api/tests/integration/health-routes.test.ts
import { describe, expect, it, vi } from "vitest";
import Fastify from "fastify";
import healthRoutes from "../../src/routes/health.routes.js";

describe("health routes", () => {
 it("returns health", async () => {
 const app = Fastify();
 app.decorate("prisma", { $queryRaw: vi.fn().mockResolvedValue([1]) } as never);
 app.decorate("redis", { ping: vi.fn().mockResolvedValue("PONG") } as never);
 await app.register(healthRoutes);
 const res = await app.inject({ method: "GET", url: "/health" });
 expect(res.statusCode).toBe(200);
 expect(res.json().status).toBe("ok");
 });

 it("returns ready", async () => {
 const app = Fastify();
 app.decorate("prisma", { $queryRaw: vi.fn().mockResolvedValue([1]) } as never);
 app.decorate("redis", { ping: vi.fn().mockResolvedValue("PONG") } as never);
 await app.register(healthRoutes);
 const res = await app.inject({ method: "GET", url: "/ready" });
 expect(res.statusCode).toBe(200);
 expect(res.json().status).toBe("ready");
 });
});
```

```typescript
// FILE: apps/api/tests/integration/auth-routes-schema.test.ts
import { describe, expect, it, vi } from "vitest";
import Fastify from "fastify";
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from "fastify-type-provider-zod";
import authRoutes from "../../src/routes/auth.routes.js";

describe("auth routes schema", () => {
 it("rejects invalid register body", async () => {
 const app = Fastify().withTypeProvider<ZodTypeProvider>();
 app.setValidatorCompiler(validatorCompiler);
 app.setSerializerCompiler(serializerCompiler);
 app.decorate("auditQueue", { add: vi.fn() } as never);
 app.decorate("prisma", {
 user: {
 findUnique: vi.fn().mockResolvedValue(null),
 create: vi.fn().mockResolvedValue({
 id: "u1",
 email: "a@example.com",
 name: "Alice",
 role: "viewer",
 version: 1,
 createdAt: new Date(),
 updatedAt: new Date()
 })
 },
 session: {
 create: vi.fn().mockResolvedValue({ id: "s1" }),
 update: vi.fn().mockResolvedValue({})
 }
 } as never);
 app.decorate("env", {
 JWT_REFRESH_TTL: "30d"
 } as never);
 await app.register(authRoutes);
 const res = await app.inject({
 method: "POST",
 url: "/auth/register",
 payload: { email: "bad", password: "123", name: "" }
 });
 expect(res.statusCode).toBe(400);
 });
});
```

```typescript
// FILE: apps/api/tests/integration/user-routes-schema.test.ts
import { describe, expect, it, vi } from "vitest";
import Fastify from "fastify";
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from "fastify-type-provider-zod";
import userRoutes from "../../src/routes/user.routes.js";

describe("user routes schema", () => {
 it("rejects invalid body before handler", async () => {
 const app = Fastify().withTypeProvider<ZodTypeProvider>();
 app.setValidatorCompiler(validatorCompiler);
 app.setSerializerCompiler(serializerCompiler);
 app.decorate("metrics", {
 authFailureCounter: { labels: vi.fn().mockReturnValue({ inc: vi.fn() }) }
 } as never);
 await app.register(userRoutes);
 const res = await app.inject({
 method: "POST",
 url: "/users",
 payload: {}
 });
 expect([400, 401]).toContain(res.statusCode);
 });
});
```

```typescript
// FILE: apps/api/tests/integration/project-routes-schema.test.ts
import { describe, expect, it, vi } from "vitest";
import Fastify from "fastify";
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from "fastify-type-provider-zod";
import projectRoutes from "../../src/routes/project.routes.js";

describe("project routes schema", () => {
 it("rejects invalid create payload", async () => {
 const app = Fastify().withTypeProvider<ZodTypeProvider>();
 app.setValidatorCompiler(validatorCompiler);
 app.setSerializerCompiler(serializerCompiler);
 app.decorate("metrics", {
 authFailureCounter: { labels: vi.fn().mockReturnValue({ inc: vi.fn() }) }
 } as never);
 await app.register(projectRoutes);
 const res = await app.inject({
 method: "POST",
 url: "/projects",
 payload: { name: "" }
 });
 expect([400, 401]).toContain(res.statusCode);
 });
});
```

```typescript
// FILE: apps/api/tests/integration/task-routes-schema.test.ts
import { describe, expect, it, vi } from "vitest";
import Fastify from "fastify";
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from "fastify-type-provider-zod";
import taskRoutes from "../../src/routes/task.routes.js";

describe("task routes schema", () => {
 it("rejects invalid transition payload", async () => {
 const app = Fastify().withTypeProvider<ZodTypeProvider>();
 app.setValidatorCompiler(validatorCompiler);
 app.setSerializerCompiler(serializerCompiler);
 app.decorate("metrics", {
 authFailureCounter: { labels: vi.fn().mockReturnValue({ inc: vi.fn() }) }
 } as never);
 await app.register(taskRoutes);
 const res = await app.inject({
 method: "POST",
 url: "/tasks/0cda2653-bdf4-4d70-abef-cfd9f61dbd4f/transition",
 payload: { status: "noop" }
 });
 expect([400, 401]).toContain(res.statusCode);
 });
});
```

```typescript
// FILE: apps/api/tests/integration/metrics-route.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import metricsPlugin from "../../src/lib/metrics.js";

describe("metrics route", () => {
 it("renders metrics output", async () => {
 const app = Fastify();
 await app.register(metricsPlugin);
 app.get("/hello", async () => ({ ok: true }));
 await app.inject({ method: "GET", url: "/hello" });
 const res = await app.inject({ method: "GET", url: "/metrics" });
 expect(res.statusCode).toBe(200);
 expect(res.body).toContain("http_requests_total");
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/app-health.e2e.test.ts
import { describe, expect, it, vi } from "vitest";
import Fastify from "fastify";
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from "fastify-type-provider-zod";
import healthRoutes from "../../src/routes/health.routes.js";
import requestContextPlugin from "../../src/plugins/request-context.js";
import metricsPlugin from "../../src/lib/metrics.js";

describe("app e2e health flow", () => {
 it("handles request-id and health", async () => {
 const app = Fastify().withTypeProvider<ZodTypeProvider>();
 app.setValidatorCompiler(validatorCompiler);
 app.setSerializerCompiler(serializerCompiler);
 app.decorate("prisma", { $queryRaw: vi.fn().mockResolvedValue([1]) } as never);
 app.decorate("redis", { ping: vi.fn().mockResolvedValue("PONG") } as never);
 await app.register(requestContextPlugin);
 await app.register(metricsPlugin);
 await app.register(healthRoutes);
 const res = await app.inject({ method: "GET", url: "/health" });
 expect(res.statusCode).toBe(200);
 expect(res.headers["x-request-id"]).toBeDefined();
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/app-metrics.e2e.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import metricsPlugin from "../../src/lib/metrics.js";

describe("app e2e metrics flow", () => {
 it("captures request metrics", async () => {
 const app = Fastify();
 await app.register(metricsPlugin);
 app.get("/ping", async () => ({ pong: true }));
 const ping = await app.inject({ method: "GET", url: "/ping" });
 expect(ping.statusCode).toBe(200);
 const metrics = await app.inject({ method: "GET", url: "/metrics" });
 expect(metrics.body).toContain("/ping");
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/websocket-hub.e2e.test.ts
import { describe, expect, it, vi } from "vitest";
import { RealtimeHub } from "../../src/realtime/hub.js";

describe("websocket hub e2e behavior", () => {
 it("broadcasts task events", () => {
 const send = vi.fn();
 const socket = {
 readyState: 1,
 send,
 on: vi.fn()
 };
 const hub = new RealtimeHub();
 hub.addClient({ id: "c1", socket: socket as never, request: {} as never });
 hub.broadcast({ type: "task.created", payload: { id: "t1", title: "Task 1" } });
 expect(send).toHaveBeenCalledWith(
 JSON.stringify({ type: "task.created", payload: { id: "t1", title: "Task 1" } })
 );
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/openapi-route.e2e.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import swaggerPlugin from "../../src/plugins/swagger.js";

describe("openapi docs route", () => {
 it("serves docs", async () => {
 const app = Fastify();
 app.decorate("env", { SWAGGER_ENABLED: true } as never);
 await app.register(swaggerPlugin);
 app.get("/a", async () => ({ ok: true }));
 await app.ready();
 const res = await app.inject({ method: "GET", url: "/docs" });
 expect([200, 302]).toContain(res.statusCode);
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/request-context.e2e.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import requestContextPlugin from "../../src/plugins/request-context.js";

describe("request context e2e", () => {
 it("propagates custom x-request-id", async () => {
 const app = Fastify();
 await app.register(requestContextPlugin);
 app.get("/", async (request) => ({ requestId: request.requestId }));
 const res = await app.inject({
 method: "GET",
 url: "/",
 headers: { "x-request-id": "custom-123" }
 });
 expect(res.json().requestId).toBe("custom-123");
 expect(res.headers["x-request-id"]).toBe("custom-123");
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/error-handler.e2e.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import { errorHandler } from "../../src/lib/errors.js";
import { AppError } from "@acme/shared";

describe("error handler e2e", () => {
 it("serializes known errors", async () => {
 const app = Fastify();
 app.setErrorHandler(errorHandler);
 app.get("/", async () => {
 throw new AppError(409, "CONFLICT", "Conflict happened");
 });
 const res = await app.inject({ method: "GET", url: "/" });
 expect(res.statusCode).toBe(409);
 expect(res.json().error.code).toBe("CONFLICT");
 });
});
```

```typescript
// FILE: apps/api/tests/e2e/security-cors.e2e.test.ts
import { describe, expect, it } from "vitest";
import Fastify from "fastify";
import securityPlugin from "../../src/plugins/security.js";

describe("security cors e2e", () => {
 it("adds cors headers", async () => {
 const app = Fastify();
 app.decorate("env", { CORS_ORIGIN: "http://localhost:3000" } as never);
 await app.register(securityPlugin);
 app.get("/", async () => ({ ok: true }));
 const res = await app.inject({
 method: "GET",
 url: "/",
 headers: { origin: "http://localhost:3000" }
 });
 expect(res.headers["access-control-allow-origin"]).toBe("http://localhost:3000");
 });
});
```
assistant: [[reply_to_current]]Bu net şekilde şu ana kadarki **en iyi çıktı**. İlk kez “production-grade’e yaklaşan” bir iskelet görüyorum.

### Model 4 – Çoklu Metrik Skor

- **1) Prompta uyum (format + kapsam): 8/10**  
  Dosya formatı disiplinli, kapsam çok geniş (monorepo, auth, RBAC, realtime, queue, metrics, swagger, docker, CI, seed, çok sayıda test).

- **2) Mimari tutarlılık: 8.5/10**  
  Plugin/repository/service/controller ayrımı iyi. Katmanlar ve sorumluluklar temiz.

- **3) Derlenebilirlik/çalıştırılabilirlik: 6.5/10**  
  Genel iskelet güçlü ama birkaç kritik risk var:  
  - Prisma’da `uuid()` kullanımı DB extension gerektirebilir (genelde `dbgenerated("gen_random_uuid()")` + extension tercih edilir).  
  - Bazı tip-genişletme ve runtime import detaylarında sürpriz hata çıkabilir.  
  - Çok dosyalı büyük yapıda “ilk çalıştırmada” küçük kırıklar normal.

- **4) Prisma/DB doğruluğu: 8/10**  
  Session, AuditLog, version alanları, index’ler ve ilişkiler iyi tasarlanmış.

- **5) Security & Auth: 8/10**  
  Access/refresh ayrımı, rotation, session revoke/reuse detection, RBAC guard, sanitize/rate-limit mevcut. Bu bölüm güçlü.

- **6) Observability/Ops: 8.5/10**  
  request-id, merkezi error handler, metrics/histogram/counter, health/ready iyi.

- **7) Test/CI/Infra: 8/10**  
  CI + Docker + compose + çok sayıda unit/integration/e2e testi var.  
  (Prompttaki “20+ test dosyası” şartını da pratikte karşılıyor.)

- **8) Kod kalitesi (strict TS, gerçek implementasyon): 7.5/10**  
  Genel kalite yüksek; bazı yerlerde `as never`/mock-heavy yaklaşım var ama kabul edilebilir.

---

## Ağırlıklı toplam: **80/100**

### Güncel sıralama
1. **Model 4: 80/100** 🥇  
2. **Model 3: 56/100**  
3. **Model 2: 26/100**  
4. **Model 1: 16/100**

Kısaca: **Model 4 açık ara lider**.  
İstersen bir sonraki adımda sana “go/no-go checklist” çıkarayım: bu kodu gerçek koşumda patlatabilecek ilk 10 teknik risk + hızlı fix planı.
