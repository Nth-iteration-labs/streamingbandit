Search.setIndex({docnames:["admin","core","eval","exp","index","libs","login","stats"],envversion:53,filenames:["admin.rst","core.rst","eval.rst","exp.rst","index.rst","libs.rst","login.rst","stats.rst"],objects:{"":{"(?i)/eval/(?P&lt;exp_id&gt;w+)/simulate":[2,0,1,"get-(?i)-eval-(?P-exp_id-w+)-simulate"],"(?i)/exp":[0,1,1,"post-(?i)-exp"],"(?i)/exp/(?P&lt;exp_id&gt;w+)":[0,3,1,"put-(?i)-exp-(?P-exp_id-w+)"],"(?i)/exp/(?P&lt;exp_id&gt;w+)/resetexperiment":[0,0,1,"get-(?i)-exp-(?P-exp_id-w+)-resetexperiment"],"(?i)/exp/defaults":[0,0,1,"get-(?i)-exp-defaults"],"(?i)/exp/defaults/(?P&lt;default_id&gt;w+)":[0,0,1,"get-(?i)-exp-defaults-(?P-default_id-w+)"],"(?i)/getaction/(?P&lt;exp_id&gt;w+)":[1,0,1,"get-(?i)-getaction-(?P-exp_id-w+)"],"(?i)/login":[6,1,1,"post-(?i)-login"],"(?i)/logout":[6,0,1,"get-(?i)-logout"],"(?i)/setreward/(?P&lt;exp_id&gt;w+)":[1,0,1,"get-(?i)-setreward-(?P-exp_id-w+)"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/actionlog":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-actionlog"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/currenttheta":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-currenttheta"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/hourlytheta":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-hourlytheta"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/log":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-log"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/rewardlog":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-rewardlog"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/simulationlog":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-simulationlog"],"(?i)/stats/(?P&lt;exp_id&gt;w+)/summary":[7,0,1,"get-(?i)-stats-(?P-exp_id-w+)-summary"],"(?i)/user":[0,1,1,"post-(?i)-user"]},"core.experiment":{Experiment:[3,5,1,""]},"core.experiment.Experiment":{__weakref__:[3,6,1,""],get_getaction_log_data:[3,7,1,""],get_hourly_theta:[3,7,1,""],get_log_data:[3,7,1,""],get_setreward_log_data:[3,7,1,""],get_simulation_log_data:[3,7,1,""],get_summary:[3,7,1,""],get_theta:[3,7,1,""],is_valid:[3,7,1,""],log_data:[3,7,1,""],log_getaction_data:[3,7,1,""],log_setreward_data:[3,7,1,""],log_simulation_data:[3,7,1,""],run_action_code:[3,7,1,""],run_context_code:[3,7,1,""],run_get_reward_code:[3,7,1,""],run_reward_code:[3,7,1,""],set_theta:[3,7,1,""]},"libs.base":{Correlation:[5,5,1,""],Count:[5,5,1,""],Covariance:[5,5,1,""],List:[5,5,1,""],Mean:[5,5,1,""],Proportion:[5,5,1,""],Variance:[5,5,1,""]},"libs.base.Correlation":{update:[5,7,1,""]},"libs.base.Count":{increment:[5,7,1,""],update:[5,7,1,""]},"libs.base.Covariance":{update:[5,7,1,""]},"libs.base.List":{__weakref__:[5,6,1,""],count:[5,7,1,""],get_dict:[5,7,1,""],max:[5,7,1,""],random:[5,7,1,""]},"libs.base.Mean":{get_count:[5,7,1,""],update:[5,7,1,""]},"libs.base.Proportion":{update:[5,7,1,""]},"libs.base.Variance":{update:[5,7,1,""]},"libs.bts":{BTS:[5,5,1,""]},"libs.bts.BTS":{__weakref__:[5,6,1,""],get_dict:[5,7,1,""],sample:[5,7,1,""],update:[5,7,1,""]},"libs.lif":{Lif:[5,5,1,""]},"libs.lif.Lif":{__init__:[5,7,1,""],__weakref__:[5,6,1,""],get_dict:[5,7,1,""],suggest:[5,7,1,""],update:[5,7,1,""]},"libs.lm":{LM:[5,5,1,""]},"libs.lm.LM":{__init__:[5,7,1,""],__weakref__:[5,6,1,""],get_coefs:[5,7,1,""],get_dict:[5,7,1,""],predict:[5,7,1,""],update:[5,7,1,""]},"libs.thompson":{BBThompsonList:[5,5,1,""],ThompsonVarList:[5,5,1,""]},"libs.thompson.BBThompsonList":{__init__:[5,7,1,""],propensity:[5,7,1,""],thompson:[5,7,1,""]},"libs.thompson.ThompsonVarList":{__init__:[5,7,1,""],experimentThompson:[5,7,1,""]},"libs.thompson_bayesian_linear":{ThompsonBayesianLinear:[5,5,1,""]},"libs.thompson_bayesian_linear.ThompsonBayesianLinear":{__weakref__:[5,6,1,""],get_dict:[5,7,1,""],sample:[5,7,1,""],update:[5,7,1,""]},core:{experiment:[3,4,0,"-"]},libs:{base:[5,4,0,"-"],bts:[5,4,0,"-"],lif:[5,4,0,"-"],lm:[5,4,0,"-"],thompson:[5,4,0,"-"],thompson_bayesian_linear:[5,4,0,"-"]}},objnames:{"0":["http","get","HTTP get"],"1":["http","post","HTTP post"],"2":["http","delete","HTTP delete"],"3":["http","put","HTTP put"],"4":["py","module","Python module"],"5":["py","class","Python class"],"6":["py","attribute","Python attribute"],"7":["py","method","Python method"]},objtypes:{"0":"http:get","1":"http:post","2":"http:delete","3":"http:put","4":"py:module","5":"py:class","6":"py:attribute","7":"py:method"},terms:{"2\u03c0n":5,"case":[4,5],"class":[3,4],"default":[0,2,4,5],"float":[3,5],"function":[4,5],"int":[0,1,2,3,5,7],"long":5,"new":[0,3,5],"return":[0,1,2,3,5,7],"true":[0,2,3,5],"try":3,Added:4,BTS:[4,5],For:[1,4],The:[0,1,2,3,4,5,6,7],__init__:5,__strmbase:4,__weakref__:[3,5],_theta:3,abl:5,abs:5,accept:4,accord:4,action:[0,1,3,5],actionlog:7,actual:3,add:[0,5],add_intercept:5,adding:5,admin:4,advic:1,advice_id:[0,1],agent:4,algorithm:[3,5],all:[0,1,2,3,4,5,7],all_float:3,alloc:5,alreadi:0,also:1,although:4,amount:[3,7],amplitud:5,ani:[4,5],api:4,arg:5,arm:5,arrai:5,arxiv:5,assign:0,assioc:3,associ:3,assum:5,automat:[3,7],avail:[0,2,4,5,7],bandit:5,base:[2,3,4],bayesian:4,bbthompsonlist:5,becaus:[3,5],behavior:3,being:5,belong:[0,2,3,7],bernoulli:5,beta:5,bodi:[0,6],bool:[0,2,3,5],bootstrap:4,bts:5,calcul:5,call:[0,1,3,6,7],can:[1,3,5],check:[0,3,5],choic:5,clear:6,close:2,code:[0,3,4],coeffici:5,com:[0,1,2,4,6,7],complet:3,condit:3,consist:[3,5,7],contact:4,contain:[0,3,5],content:3,context:[0,1,3],control:5,convert:3,cooki:[0,2,6,7],core:[3,4],correctli:3,correl:5,correspond:1,count:5,counter:5,cov:5,covari:5,creat:[0,2,3,5],current:[1,3,4,5,7],currenttheta:7,data:[2,3,5,7],databas:[2,3,5],date:[3,4,7],david:5,debug:1,decis:5,default_id:0,default_param:5,default_reward:0,defin:[3,5],definit:5,delet:0,delta_hour:0,dese:5,determin:3,develop:4,deviat:5,dict:[0,3,5,7],dictionari:[3,5],differ:[3,5],discount:5,displai:2,distinguish:3,distribut:5,doe:[0,2,7],dot:4,doubl:5,draw:[2,5,6],duplic:0,each:[3,5],edit:0,effect:5,either:5,empti:5,enough:5,error:[0,5],estim:5,eval:2,evalu:[1,4],everi:3,exampl:[0,1,2,4,6,7],exec:3,execut:3,exist:0,exp:0,exp_id:[0,1,2,3,7],expand:4,expect:5,experi:[0,1,2,4,6,7],experimentthompson:5,expriment:0,fals:[2,3,5],feedback:[2,4],find:5,first:[1,4],fit:5,flag:[2,3],folder:4,follow:[1,4,5],form:[0,5],four:2,free:3,from:[1,3,5],full:1,gamma:5,gener:3,get:[0,1,2,3,6,7],get_act:[0,3,7],get_coef:5,get_context:[0,3],get_count:5,get_dict:[3,5],get_getaction_log_data:3,get_hourly_theta:3,get_log_data:3,get_reward:[0,3],get_setreward_log_data:3,get_simulation_log_data:3,get_summari:3,get_theta:3,getact:[0,1,3],getadvic:0,getcontext:0,getreward:0,give:[0,3],given:[1,3,5],gladli:4,gmail:4,group:5,handler:6,has:[3,5],have:[0,1,4,6],here:5,hour:0,hourli:[0,3,7],hourly_theta:0,hourlytheta:7,how:5,http:[0,1,2,5,6,7],iannuzzi:5,implement:5,includ:1,increment:5,indic:[0,1,2],info:0,inform:[1,4],initi:5,instanc:5,integr:5,interact:3,intercept:5,interpet:5,invalid:1,is_valid:3,itself:5,json:[0,1,2,6,7],jule:4,juleskruijswijk:4,kaptein:[4,5],kei:[0,1,3],kruijswijk:4,kwarg:5,last:[3,7],later:1,learnrat:5,leav:5,lib:[4,5],lif:[4,5],lifvers:5,like:[4,5],limit:[0,3,7],linear:4,list:[0,3,5,7],lock:4,log:[0,2,3,7],log_data:3,log_getaction_data:3,log_setreward_data:3,log_simulation_data:3,log_stat:2,login:[4,6],logout:6,look:[4,5],loop:[1,2,3],made:[4,5],mai:[3,5],main:5,mandatori:1,manual:[1,3,7],match:3,maurit:[4,5],mauritskaptein:4,max:5,maxim:5,mean:[1,5],messag:0,method:5,minim:5,model:5,mongodb:3,multipl:5,must:3,name:[0,3,5],need:[3,5],next:1,nois:5,noisesd:5,none:[3,5],normal:5,noth:5,notusedforloopback:3,number:[0,2,3,5,6,7],numpi:[2,5],object:[0,2,3,5,6,7],observ:5,obtain:[0,2,5,7],okai:3,omega:5,one:3,onli:[1,3],onlin:5,option:[0,1,2,7],org:5,organ:3,oscil:5,other:3,otherwis:3,outcom:5,output:5,over:[0,5],pair:0,param:5,param_nois:5,paramet:[0,1,2,3,5,6,7],pars:5,part:4,password:[0,6],pick:5,point:4,polici:5,possibl:5,post:[0,6],pre:3,precis:5,predict:5,prefer:0,propens:5,properti:[0,1],proport:5,provid:[3,5],put:0,python:[0,3],rais:[0,1,2,6,7],random:5,rate:5,receiv:1,redi:3,refer:[3,5],regress:4,regressor:5,releas:4,repres:5,requir:[0,2,7],reset:0,resetexperi:0,result:2,retriev:[0,6,7],reward:[0,1,3],rewardlog:7,run:0,run_action_cod:3,run_context_cod:3,run_get_reward_cod:3,run_reward_cod:3,sampl:4,sampler:5,save:5,script:2,second:[1,4],secur:[0,2,6,7],see:5,seed:2,sequenti:5,server:0,set:[0,1,2,3,6,7],set_reward:[0,3,7],set_theta:3,setreward:[0,1],should:[0,5],show:0,simplifi:5,simul:[2,3,6,7],simulationlog:7,sinc:3,size:5,skeleton:4,solut:5,specif:[0,1],specifi:[1,2,3,6],standard:[1,5],start:5,stat:7,state:0,statist:4,still:4,store:[0,3,5],streamingbandit:0,string:[0,1,3,5,6],subject:5,success:[0,1,2],suggest:5,summari:[3,7],suppli:[0,1],take:3,tbl:4,test:[4,5],them:4,theta:[0,3,5,7],theta_kei:0,theta_valu:0,thi:[0,2,3,5,7],thompson:4,thompson_bayesian_linear:5,thompsonbayesianlinear:5,thompsonvarlist:5,tied:3,time:5,toggl:1,total:5,two:[1,5],type:[3,5],typic:3,under:4,unequ:5,updat:[1,5],update_method:5,url:[1,2,6],use:4,used:[0,1,3,5],user:[0,2,3,7],usernam:[0,6],uses:[4,5],using:5,util:4,valid:[0,3],valu:[0,3,5],value_nam:5,variabl:[3,5],varianc:5,vector:5,verbos:2,version:[3,4,5],weak:[3,5],well:1,whatnot:5,when:[0,1,2,5],wheter:3,whether:[0,3],which:[2,3,5],within:[3,5],would:4,write:4,written:4,wrong:[0,2,6,7],x_bar:5,x_s:5,x_v:5,y_bar:5,y_s:5,y_v:5,yet:5,you:[1,4,5],your:[2,5]},titles:["Admin API","Core API","Evaluation API","Experiment functions","Welcome to StreamingBandit\u2019s documentation!","Documentation of the supplied Libraries","Management API","Statistics API"],titleterms:{"class":5,"function":3,admin:0,api:[0,1,2,6,7],author:4,base:5,bayesian:5,bootstrap:5,changelog:4,contribut:4,core:1,document:[4,5],evalu:2,experi:3,feedback:5,librari:[4,5],linear:5,lock:5,manag:6,regress:5,sampl:5,statist:7,streamingbandit:4,suppli:5,thompson:5,welcom:4}})