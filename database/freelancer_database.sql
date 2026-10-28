USE [master]
GO
IF DB_ID(N'freelancer') IS NULL
    CREATE DATABASE [freelancer];
GO
USE [freelancer]
GO
USE [freelancer]
GO
/****** Object:  Table [dbo].[AdminAccounts]    Script Date: 10/28/2026 10:01:49 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AdminAccounts](
	[UserId] [int] NOT NULL,
	[GrantedAt] [datetime2](7) NOT NULL,
 CONSTRAINT [PK_AdminAccounts] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Categories]    Script Date: 10/28/2026 10:01:49 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Categories](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](100) NOT NULL,
 CONSTRAINT [PK_Categories] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Certificates]    Script Date: 10/28/2026 10:01:49 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Certificates](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[UserId] [int] NOT NULL,
	[Title] [nvarchar](150) NOT NULL,
	[Issuer] [nvarchar](150) NULL,
	[IssueDate] [date] NULL,
	[CertificateUrl] [nvarchar](500) NULL,
 CONSTRAINT [PK_Certificates] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PortfolioItems]    Script Date: 10/28/2026 10:01:49 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PortfolioItems](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[UserId] [int] NOT NULL,
	[Title] [nvarchar](150) NOT NULL,
	[Description] [nvarchar](1000) NULL,
	[Url] [nvarchar](500) NULL,
	[CreatedAt] [datetime2](7) NOT NULL,
 CONSTRAINT [PK_PortfolioItems] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[project]    Script Date: 10/28/2026 10:01:49 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[project](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[title] [nvarchar](50) NOT NULL,
	[description] [nvarchar](max) NOT NULL,
	[budget] [int] NOT NULL,
	[client-id] [int] NOT NULL,
	[PricingType] [varchar](20) NOT NULL,
	[ProjectStatus] [varchar](20) NOT NULL,
	[CreatedAt] [datetime2](7) NOT NULL,
	[UpdatedAt] [datetime2](7) NOT NULL,
	[Deadline] [date] NULL,
 CONSTRAINT [PK_project] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ProjectCategories]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ProjectCategories](
	[ProjectId] [int] NOT NULL,
	[CategoryId] [int] NOT NULL,
 CONSTRAINT [PK_ProjectCategories] PRIMARY KEY CLUSTERED 
(
	[ProjectId] ASC,
	[CategoryId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ProjectSkills]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ProjectSkills](
	[ProjectId] [int] NOT NULL,
	[SkillId] [int] NOT NULL,
 CONSTRAINT [PK_ProjectSkills] PRIMARY KEY CLUSTERED 
(
	[ProjectId] ASC,
	[SkillId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[proposal]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[proposal](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[cover-letter] [nvarchar](max) NOT NULL,
	[EstimatedDurationDays] [int] NOT NULL,
	[freelancer-id] [int] NOT NULL,
	[project-id] [int] NOT NULL,
	[budget] [int] NOT NULL,
	[status] [varchar](20) NOT NULL,
	[CreatedAt] [datetime2](7) NOT NULL,
 CONSTRAINT [PK_proposal] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Skills]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Skills](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [nvarchar](100) NOT NULL,
 CONSTRAINT [PK_Skills] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[user]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[user](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
	[phone] [varchar](50) NULL,
	[address] [nvarchar](250) NOT NULL,
	[email] [varchar](100) NOT NULL,
	[codemeli] [varchar](20) NOT NULL,
	[PasswordHash] [nvarchar](255) NOT NULL,
	[AccountStatus] [varchar](10) NOT NULL,
	[CreatedAt] [datetime2](7) NOT NULL,
	[UpdatedAt] [datetime2](7) NOT NULL,
 CONSTRAINT [PK_user] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[UserProfiles]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[UserProfiles](
	[UserId] [int] NOT NULL,
	[ProfessionalTitle] [nvarchar](100) NULL,
	[Bio] [nvarchar](1000) NULL,
	[Location] [nvarchar](150) NULL,
 CONSTRAINT [PK_UserProfiles] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[UserSkills]    Script Date: 10/28/2026 10:01:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[UserSkills](
	[UserId] [int] NOT NULL,
	[SkillId] [int] NOT NULL,
 CONSTRAINT [PK_UserSkills] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC,
	[SkillId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[AdminAccounts] ([UserId], [GrantedAt]) VALUES (1, CAST(N'2026-10-28T21:15:58.6092439' AS DateTime2))
GO
SET IDENTITY_INSERT [dbo].[Categories] ON 

INSERT [dbo].[Categories] ([Id], [Title]) VALUES (2, N'برنامه‌نویسی')
INSERT [dbo].[Categories] ([Id], [Title]) VALUES (1, N'طراحی سایت')
INSERT [dbo].[Categories] ([Id], [Title]) VALUES (3, N'طراحی گرافیک')
SET IDENTITY_INSERT [dbo].[Categories] OFF
GO
SET IDENTITY_INSERT [dbo].[Certificates] ON 

INSERT [dbo].[Certificates] ([Id], [UserId], [Title], [Issuer], [IssueDate], [CertificateUrl]) VALUES (1, 2, N'مبانی طراحی وب', N'آموزشگاه نمونه', CAST(N'2025-06-15' AS Date), N'https://example.com/certificates/web')
INSERT [dbo].[Certificates] ([Id], [UserId], [Title], [Issuer], [IssueDate], [CertificateUrl]) VALUES (2, 3, N'مبانی برنامه‌نویسی پایتون', N'آموزشگاه نمونه', CAST(N'2025-08-20' AS Date), N'https://example.com/certificates/python')
SET IDENTITY_INSERT [dbo].[Certificates] OFF
GO
SET IDENTITY_INSERT [dbo].[PortfolioItems] ON 

INSERT [dbo].[PortfolioItems] ([Id], [UserId], [Title], [Description], [Url], [CreatedAt]) VALUES (1, 2, N'فروشگاه اینترنتی نمونه', N'نمونه‌کار طراحی و پیاده‌سازی فروشگاه اینترنتی.', N'https://example.com/portfolio/shop', CAST(N'2026-10-28T21:18:57.8139340' AS DateTime2))
INSERT [dbo].[PortfolioItems] ([Id], [UserId], [Title], [Description], [Url], [CreatedAt]) VALUES (2, 3, N'برنامه مدیریت وظایف', N'نمونه‌کار برنامه‌نویسی برای مدیریت وظایف روزانه.', N'https://example.com/portfolio/tasks', CAST(N'2026-10-28T21:18:57.8139340' AS DateTime2))
SET IDENTITY_INSERT [dbo].[PortfolioItems] OFF
GO
SET IDENTITY_INSERT [dbo].[project] ON 

INSERT [dbo].[project] ([id], [title], [description], [budget], [client-id], [PricingType], [ProjectStatus], [CreatedAt], [UpdatedAt], [Deadline]) VALUES (1, N'طراحی سایت فروشگاهی', N'طراحی و پیاده‌سازی یک سایت فروشگاهی واکنش‌گرا.', 15000000, 2, N'Fixed Price', N'In Progress', CAST(N'2026-10-28T21:17:22.2246571' AS DateTime2), CAST(N'2026-10-28T21:18:30.7335935' AS DateTime2), CAST(N'2026-12-15' AS Date))
INSERT [dbo].[project] ([id], [title], [description], [budget], [client-id], [PricingType], [ProjectStatus], [CreatedAt], [UpdatedAt], [Deadline]) VALUES (2, N'برنامه مدیریت وظایف', N'ساخت برنامه‌ای ساده برای مدیریت و پیگیری وظایف.', 8000000, 3, N'Fixed Price', N'Open', CAST(N'2026-10-28T21:17:22.2246571' AS DateTime2), CAST(N'2026-10-28T21:17:22.2246571' AS DateTime2), CAST(N'2026-12-20' AS Date))
INSERT [dbo].[project] ([id], [title], [description], [budget], [client-id], [PricingType], [ProjectStatus], [CreatedAt], [UpdatedAt], [Deadline]) VALUES (3, N'طراحی رابط کاربری اپلیکیشن', N'طراحی رابط کاربری اپلیکیشن موبایل.', 500000, 4, N'Hourly', N'Open', CAST(N'2026-10-28T21:17:22.2246571' AS DateTime2), CAST(N'2026-10-28T21:17:22.2246571' AS DateTime2), CAST(N'2026-12-25' AS Date))
SET IDENTITY_INSERT [dbo].[project] OFF
GO
INSERT [dbo].[ProjectCategories] ([ProjectId], [CategoryId]) VALUES (1, 1)
INSERT [dbo].[ProjectCategories] ([ProjectId], [CategoryId]) VALUES (2, 2)
INSERT [dbo].[ProjectCategories] ([ProjectId], [CategoryId]) VALUES (3, 3)
GO
INSERT [dbo].[ProjectSkills] ([ProjectId], [SkillId]) VALUES (1, 1)
INSERT [dbo].[ProjectSkills] ([ProjectId], [SkillId]) VALUES (1, 2)
INSERT [dbo].[ProjectSkills] ([ProjectId], [SkillId]) VALUES (2, 3)
INSERT [dbo].[ProjectSkills] ([ProjectId], [SkillId]) VALUES (2, 5)
INSERT [dbo].[ProjectSkills] ([ProjectId], [SkillId]) VALUES (3, 4)
GO
SET IDENTITY_INSERT [dbo].[proposal] ON 

INSERT [dbo].[proposal] ([id], [cover-letter], [EstimatedDurationDays], [freelancer-id], [project-id], [budget], [status], [CreatedAt]) VALUES (1, N'تجربه کافی در طراحی سایت دارم و پروژه را با کیفیت انجام می‌دهم.', 10, 3, 1, 14000000, N'Accepted', CAST(N'2026-10-28T21:18:15.8463842' AS DateTime2))
INSERT [dbo].[proposal] ([id], [cover-letter], [EstimatedDurationDays], [freelancer-id], [project-id], [budget], [status], [CreatedAt]) VALUES (2, N'می‌توانم این پروژه را با استفاده از مهارت‌های برنامه‌نویسی انجام دهم.', 7, 4, 2, 7500000, N'Pending', CAST(N'2026-10-28T21:18:15.8463842' AS DateTime2))
INSERT [dbo].[proposal] ([id], [cover-letter], [EstimatedDurationDays], [freelancer-id], [project-id], [budget], [status], [CreatedAt]) VALUES (3, N'برای طراحی رابط کاربری، طرحی ساده و کاربردی ارائه می‌کنم.', 5, 2, 3, 450000, N'Pending', CAST(N'2026-10-28T21:18:15.8463842' AS DateTime2))
INSERT [dbo].[proposal] ([id], [cover-letter], [EstimatedDurationDays], [freelancer-id], [project-id], [budget], [status], [CreatedAt]) VALUES (4, N'می‌توانم سایت فروشگاهی را با طراحی واکنش‌گرا پیاده‌سازی کنم.', 12, 4, 1, 14500000, N'Pending', CAST(N'2026-10-28T21:18:15.8463842' AS DateTime2))
SET IDENTITY_INSERT [dbo].[proposal] OFF
GO
SET IDENTITY_INSERT [dbo].[Skills] ON 

INSERT [dbo].[Skills] ([Id], [Name]) VALUES (1, N'HTML و CSS')
INSERT [dbo].[Skills] ([Id], [Name]) VALUES (2, N'JavaScript')
INSERT [dbo].[Skills] ([Id], [Name]) VALUES (3, N'Python')
INSERT [dbo].[Skills] ([Id], [Name]) VALUES (5, N'SQL Server')
INSERT [dbo].[Skills] ([Id], [Name]) VALUES (4, N'طراحی رابط کاربری')
SET IDENTITY_INSERT [dbo].[Skills] OFF
GO
SET IDENTITY_INSERT [dbo].[user] ON 

INSERT [dbo].[user] ([id], [name], [phone], [address], [email], [codemeli], [PasswordHash], [AccountStatus], [CreatedAt], [UpdatedAt]) VALUES (1, N'علی رضایی', N'09120000001', N'تهران', N'ali@example.com', N'0012345678', N'demo_hash_user_1', N'Active', CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2), CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2))
INSERT [dbo].[user] ([id], [name], [phone], [address], [email], [codemeli], [PasswordHash], [AccountStatus], [CreatedAt], [UpdatedAt]) VALUES (2, N'سارا احمدی', N'09120000002', N'اصفهان', N'sara@example.com', N'0023456789', N'demo_hash_user_2', N'Active', CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2), CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2))
INSERT [dbo].[user] ([id], [name], [phone], [address], [email], [codemeli], [PasswordHash], [AccountStatus], [CreatedAt], [UpdatedAt]) VALUES (3, N'محمد کریمی', N'09120000003', N'شیراز', N'mohammad@example.com', N'0034567890', N'demo_hash_user_3', N'Active', CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2), CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2))
INSERT [dbo].[user] ([id], [name], [phone], [address], [email], [codemeli], [PasswordHash], [AccountStatus], [CreatedAt], [UpdatedAt]) VALUES (4, N'نگار موسوی', N'09120000004', N'تبریز', N'negar@example.com', N'0045678901', N'demo_hash_user_4', N'Active', CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2), CAST(N'2026-10-28T21:15:32.8127736' AS DateTime2))
SET IDENTITY_INSERT [dbo].[user] OFF
GO
INSERT [dbo].[UserProfiles] ([UserId], [ProfessionalTitle], [Bio], [Location]) VALUES (2, N'طراح و توسعه‌دهنده وب', N'علاقه‌مند به طراحی و توسعه وب‌سایت.', N'تهران')
INSERT [dbo].[UserProfiles] ([UserId], [ProfessionalTitle], [Bio], [Location]) VALUES (3, N'برنامه‌نویس پایتون', N'فعال در زمینه برنامه‌نویسی و توسعه نرم‌افزار.', N'اصفهان')
INSERT [dbo].[UserProfiles] ([UserId], [ProfessionalTitle], [Bio], [Location]) VALUES (4, N'طراح رابط کاربری', N'علاقه‌مند به طراحی رابط کاربری و تجربه کاربری.', N'شیراز')
GO
INSERT [dbo].[UserSkills] ([UserId], [SkillId]) VALUES (2, 1)
INSERT [dbo].[UserSkills] ([UserId], [SkillId]) VALUES (2, 2)
INSERT [dbo].[UserSkills] ([UserId], [SkillId]) VALUES (3, 3)
INSERT [dbo].[UserSkills] ([UserId], [SkillId]) VALUES (3, 5)
INSERT [dbo].[UserSkills] ([UserId], [SkillId]) VALUES (4, 1)
INSERT [dbo].[UserSkills] ([UserId], [SkillId]) VALUES (4, 4)
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ_Categories_Title]    Script Date: 10/28/2026 10:01:50 PM ******/
ALTER TABLE [dbo].[Categories] ADD  CONSTRAINT [UQ_Categories_Title] UNIQUE NONCLUSTERED 
(
	[Title] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [UQ_Proposal_Freelancer_Project]    Script Date: 10/28/2026 10:01:50 PM ******/
ALTER TABLE [dbo].[proposal] ADD  CONSTRAINT [UQ_Proposal_Freelancer_Project] UNIQUE NONCLUSTERED 
(
	[freelancer-id] ASC,
	[project-id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ_Skills_Name]    Script Date: 10/28/2026 10:01:50 PM ******/
ALTER TABLE [dbo].[Skills] ADD  CONSTRAINT [UQ_Skills_Name] UNIQUE NONCLUSTERED 
(
	[Name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ_User_Codemeli]    Script Date: 10/28/2026 10:01:50 PM ******/
ALTER TABLE [dbo].[user] ADD  CONSTRAINT [UQ_User_Codemeli] UNIQUE NONCLUSTERED 
(
	[codemeli] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ_User_Email]    Script Date: 10/28/2026 10:01:50 PM ******/
ALTER TABLE [dbo].[user] ADD  CONSTRAINT [UQ_User_Email] UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UX_User_Phone_NotNull]    Script Date: 10/28/2026 10:01:50 PM ******/
CREATE UNIQUE NONCLUSTERED INDEX [UX_User_Phone_NotNull] ON [dbo].[user]
(
	[phone] ASC
)
WHERE ([Phone] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[AdminAccounts] ADD  CONSTRAINT [DF_AdminAccounts_GrantedAt]  DEFAULT (sysdatetime()) FOR [GrantedAt]
GO
ALTER TABLE [dbo].[PortfolioItems] ADD  CONSTRAINT [DF_PortfolioItems_CreatedAt]  DEFAULT (sysdatetime()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[project] ADD  CONSTRAINT [DF_Project_PricingType]  DEFAULT ('Fixed Price') FOR [PricingType]
GO
ALTER TABLE [dbo].[project] ADD  CONSTRAINT [DF_Project_ProjectStatus]  DEFAULT ('Draft') FOR [ProjectStatus]
GO
ALTER TABLE [dbo].[project] ADD  CONSTRAINT [DF_Project_CreatedAt]  DEFAULT (sysdatetime()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[project] ADD  CONSTRAINT [DF_Project_UpdatedAt]  DEFAULT (sysdatetime()) FOR [UpdatedAt]
GO
ALTER TABLE [dbo].[proposal] ADD  CONSTRAINT [DF_Proposal_Status]  DEFAULT ('Pending') FOR [status]
GO
ALTER TABLE [dbo].[proposal] ADD  CONSTRAINT [DF_Proposal_CreatedAt]  DEFAULT (sysdatetime()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[user] ADD  CONSTRAINT [DF_User_AccountStatus]  DEFAULT ('Active') FOR [AccountStatus]
GO
ALTER TABLE [dbo].[user] ADD  CONSTRAINT [DF_User_CreatedAt]  DEFAULT (sysdatetime()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[user] ADD  CONSTRAINT [DF_User_UpdatedAt]  DEFAULT (sysdatetime()) FOR [UpdatedAt]
GO
ALTER TABLE [dbo].[AdminAccounts]  WITH CHECK ADD  CONSTRAINT [FK_AdminAccounts_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[AdminAccounts] CHECK CONSTRAINT [FK_AdminAccounts_User]
GO
ALTER TABLE [dbo].[Certificates]  WITH CHECK ADD  CONSTRAINT [FK_Certificates_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[Certificates] CHECK CONSTRAINT [FK_Certificates_User]
GO
ALTER TABLE [dbo].[PortfolioItems]  WITH CHECK ADD  CONSTRAINT [FK_PortfolioItems_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[PortfolioItems] CHECK CONSTRAINT [FK_PortfolioItems_User]
GO
ALTER TABLE [dbo].[project]  WITH CHECK ADD  CONSTRAINT [FK_project_user] FOREIGN KEY([client-id])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[project] CHECK CONSTRAINT [FK_project_user]
GO
ALTER TABLE [dbo].[ProjectCategories]  WITH CHECK ADD  CONSTRAINT [FK_ProjectCategories_Category] FOREIGN KEY([CategoryId])
REFERENCES [dbo].[Categories] ([Id])
GO
ALTER TABLE [dbo].[ProjectCategories] CHECK CONSTRAINT [FK_ProjectCategories_Category]
GO
ALTER TABLE [dbo].[ProjectCategories]  WITH CHECK ADD  CONSTRAINT [FK_ProjectCategories_Project] FOREIGN KEY([ProjectId])
REFERENCES [dbo].[project] ([id])
GO
ALTER TABLE [dbo].[ProjectCategories] CHECK CONSTRAINT [FK_ProjectCategories_Project]
GO
ALTER TABLE [dbo].[ProjectSkills]  WITH CHECK ADD  CONSTRAINT [FK_ProjectSkills_Project] FOREIGN KEY([ProjectId])
REFERENCES [dbo].[project] ([id])
GO
ALTER TABLE [dbo].[ProjectSkills] CHECK CONSTRAINT [FK_ProjectSkills_Project]
GO
ALTER TABLE [dbo].[ProjectSkills]  WITH CHECK ADD  CONSTRAINT [FK_ProjectSkills_Skill] FOREIGN KEY([SkillId])
REFERENCES [dbo].[Skills] ([Id])
GO
ALTER TABLE [dbo].[ProjectSkills] CHECK CONSTRAINT [FK_ProjectSkills_Skill]
GO
ALTER TABLE [dbo].[proposal]  WITH CHECK ADD  CONSTRAINT [FK_Proposal_Project] FOREIGN KEY([project-id])
REFERENCES [dbo].[project] ([id])
GO
ALTER TABLE [dbo].[proposal] CHECK CONSTRAINT [FK_Proposal_Project]
GO
ALTER TABLE [dbo].[proposal]  WITH CHECK ADD  CONSTRAINT [FK_Proposal_User] FOREIGN KEY([freelancer-id])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[proposal] CHECK CONSTRAINT [FK_Proposal_User]
GO
ALTER TABLE [dbo].[UserProfiles]  WITH CHECK ADD  CONSTRAINT [FK_UserProfiles_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[UserProfiles] CHECK CONSTRAINT [FK_UserProfiles_User]
GO
ALTER TABLE [dbo].[UserSkills]  WITH CHECK ADD  CONSTRAINT [FK_UserSkills_Skill] FOREIGN KEY([SkillId])
REFERENCES [dbo].[Skills] ([Id])
GO
ALTER TABLE [dbo].[UserSkills] CHECK CONSTRAINT [FK_UserSkills_Skill]
GO
ALTER TABLE [dbo].[UserSkills]  WITH CHECK ADD  CONSTRAINT [FK_UserSkills_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[UserSkills] CHECK CONSTRAINT [FK_UserSkills_User]
GO
ALTER TABLE [dbo].[project]  WITH CHECK ADD  CONSTRAINT [CK_Project_Budget] CHECK  (([Budget]>(0)))
GO
ALTER TABLE [dbo].[project] CHECK CONSTRAINT [CK_Project_Budget]
GO
ALTER TABLE [dbo].[project]  WITH CHECK ADD  CONSTRAINT [CK_Project_Description] CHECK  ((len(ltrim(rtrim([Description])))>(0)))
GO
ALTER TABLE [dbo].[project] CHECK CONSTRAINT [CK_Project_Description]
GO
ALTER TABLE [dbo].[project]  WITH CHECK ADD  CONSTRAINT [CK_Project_PricingType] CHECK  (([PricingType]='Fixed Price' OR [PricingType]='Hourly'))
GO
ALTER TABLE [dbo].[project] CHECK CONSTRAINT [CK_Project_PricingType]
GO
ALTER TABLE [dbo].[project]  WITH CHECK ADD  CONSTRAINT [CK_Project_ProjectStatus] CHECK  (([ProjectStatus]='Cancelled' OR [ProjectStatus]='Completed' OR [ProjectStatus]='In Progress' OR [ProjectStatus]='Open' OR [ProjectStatus]='Draft'))
GO
ALTER TABLE [dbo].[project] CHECK CONSTRAINT [CK_Project_ProjectStatus]
GO
ALTER TABLE [dbo].[project]  WITH CHECK ADD  CONSTRAINT [CK_Project_Title] CHECK  ((len(ltrim(rtrim([Title])))>(0)))
GO
ALTER TABLE [dbo].[project] CHECK CONSTRAINT [CK_Project_Title]
GO
ALTER TABLE [dbo].[proposal]  WITH CHECK ADD  CONSTRAINT [CK_Proposal_Budget] CHECK  (([Budget]>(0)))
GO
ALTER TABLE [dbo].[proposal] CHECK CONSTRAINT [CK_Proposal_Budget]
GO
ALTER TABLE [dbo].[proposal]  WITH CHECK ADD  CONSTRAINT [CK_Proposal_EstimatedDurationDays] CHECK  (([EstimatedDurationDays]>(0)))
GO
ALTER TABLE [dbo].[proposal] CHECK CONSTRAINT [CK_Proposal_EstimatedDurationDays]
GO
ALTER TABLE [dbo].[proposal]  WITH CHECK ADD  CONSTRAINT [CK_Proposal_Status] CHECK  (([Status]='Withdrawn' OR [Status]='Rejected' OR [Status]='Accepted' OR [Status]='Pending'))
GO
ALTER TABLE [dbo].[proposal] CHECK CONSTRAINT [CK_Proposal_Status]
GO
ALTER TABLE [dbo].[user]  WITH CHECK ADD  CONSTRAINT [CK_User_AccountStatus] CHECK  (([AccountStatus]='Blocked' OR [AccountStatus]='Inactive' OR [AccountStatus]='Active'))
GO
ALTER TABLE [dbo].[user] CHECK CONSTRAINT [CK_User_AccountStatus]
GO
ALTER TABLE [dbo].[user]  WITH CHECK ADD  CONSTRAINT [CK_User_Codemeli] CHECK  ((len([Codemeli])=(10) AND NOT [Codemeli] like '%[^0-9]%'))
GO
ALTER TABLE [dbo].[user] CHECK CONSTRAINT [CK_User_Codemeli]
GO
ALTER TABLE [dbo].[user]  WITH CHECK ADD  CONSTRAINT [CK_User_Email] CHECK  (([Email] like '%_@_%._%' AND NOT [Email] like '% %'))
GO
ALTER TABLE [dbo].[user] CHECK CONSTRAINT [CK_User_Email]
GO
ALTER TABLE [dbo].[user]  WITH CHECK ADD  CONSTRAINT [CK_User_Name] CHECK  ((len(ltrim(rtrim([Name])))>(0)))
GO
ALTER TABLE [dbo].[user] CHECK CONSTRAINT [CK_User_Name]
GO
ALTER TABLE [dbo].[user]  WITH CHECK ADD  CONSTRAINT [CK_User_Phone] CHECK  (([Phone] IS NULL OR len([Phone])=(11) AND [Phone] like '09[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'))
GO
ALTER TABLE [dbo].[user] CHECK CONSTRAINT [CK_User_Phone]
GO

-- Triggers
GO
CREATE TRIGGER dbo.TR_Project_PreventAdminInsert
ON dbo.Project
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN dbo.AdminAccounts a ON a.UserId = i.[client-id]
    )
    BEGIN
        ROLLBACK TRANSACTION;
        THROW 50001, 'Admin accounts cannot create projects.', 1;
    END;
END;
GO

CREATE TRIGGER dbo.TR_Project_UpdateUpdatedAt
ON dbo.Project
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE p
    SET UpdatedAt = SYSDATETIME()
    FROM dbo.Project p
    INNER JOIN inserted i ON p.Id = i.Id;
END;
GO

CREATE TRIGGER dbo.TR_Proposal_OnlyOneAccepted
ON dbo.proposal
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (
        SELECT 1
        FROM dbo.proposal p
        WHERE p.Status = 'Accepted'
          AND EXISTS (
              SELECT 1
              FROM inserted i
              WHERE i.[project-id] = p.[project-id]
          )
        GROUP BY p.[project-id]
        HAVING COUNT(*) > 1
    )
    BEGIN
        ROLLBACK TRANSACTION;
        THROW 50005, 'Only one proposal can be accepted per project.', 1;
    END;
END;
GO

CREATE TRIGGER dbo.TR_Proposal_PreventAdminInsert
ON dbo.proposal
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN dbo.AdminAccounts a ON a.UserId = i.[freelancer-id]
    )
    BEGIN
        ROLLBACK TRANSACTION;
        THROW 50002, 'Admin accounts cannot submit proposals.', 1;
    END;
END;
GO

CREATE TRIGGER dbo.TR_Proposal_UpdateProjectStatus
ON dbo.proposal
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE p
    SET ProjectStatus = 'In Progress'
    FROM dbo.Project p
    INNER JOIN inserted i ON p.Id = i.[project-id]
    WHERE i.Status = 'Accepted';
END;
GO

CREATE TRIGGER dbo.TR_Proposal_ValidateInsert
ON dbo.proposal
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN dbo.Project p ON p.Id = i.[project-id]
        WHERE p.[client-id] = i.[freelancer-id]
    )
    BEGIN
        ROLLBACK TRANSACTION;
        THROW 50003, 'A user cannot submit a proposal to their own project.', 1;
    END;

    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN dbo.Project p ON p.Id = i.[project-id]
        WHERE p.ProjectStatus <> 'Open'
    )
    BEGIN
        ROLLBACK TRANSACTION;
        THROW 50004, 'Proposals can only be submitted to open projects.', 1;
    END;
END;
GO

CREATE TRIGGER dbo.TR_User_UpdateUpdatedAt
ON dbo.[User]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE u
    SET UpdatedAt = SYSDATETIME()
    FROM dbo.[User] u
    INNER JOIN inserted i ON u.Id = i.Id;
END;
GO
